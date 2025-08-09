#!/usr/bin/env python3
"""File lock manager for SPARK parallel execution"""

import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class FileLockManager:
    """Manages file locks for parallel team execution"""
    
    LOCK_FILE = Path(".claude/workflows/file_locks.json")
    LOCK_TIMEOUT = 30  # seconds
    
    @classmethod
    def _load_locks(cls) -> Dict[str, Any]:
        """Load current lock state"""
        if not cls.LOCK_FILE.exists():
            cls.LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
            return {}
        
        try:
            with open(cls.LOCK_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    @classmethod
    def _save_locks(cls, locks: Dict[str, Any]) -> None:
        """Save lock state"""
        cls.LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(cls.LOCK_FILE, 'w') as f:
            json.dump(locks, f, indent=2)
    
    @classmethod
    def acquire_lock(cls, file_path: str, team_id: str, timeout: int = 5) -> bool:
        """
        Attempt to acquire a lock on a file
        
        Args:
            file_path: Path to the file to lock
            team_id: ID of the team requesting the lock
            timeout: Maximum seconds to wait for lock
            
        Returns:
            bool: True if lock acquired, False otherwise
        """
        start_time = time.time()
        backoff = 0.1
        
        while time.time() - start_time < timeout:
            locks = cls._load_locks()
            
            # Clean expired locks
            current_time = datetime.now()
            for path, lock_info in list(locks.items()):
                lock_time = datetime.fromisoformat(lock_info["timestamp"])
                if current_time - lock_time > timedelta(seconds=cls.LOCK_TIMEOUT):
                    del locks[path]
            
            # Check if file is locked
            if file_path in locks:
                if locks[file_path]["team_id"] == team_id:
                    # Already own the lock
                    return True
                # Wait with exponential backoff
                time.sleep(min(backoff, 2.0))
                backoff *= 1.5
                continue
            
            # Acquire lock
            locks[file_path] = {
                "team_id": team_id,
                "timestamp": datetime.now().isoformat()
            }
            cls._save_locks(locks)
            return True
        
        return False
    
    @classmethod
    def release_lock(cls, file_path: str, team_id: str) -> bool:
        """
        Release a lock on a file
        
        Args:
            file_path: Path to the file to unlock
            team_id: ID of the team releasing the lock
            
        Returns:
            bool: True if lock released, False if not owned
        """
        locks = cls._load_locks()
        
        if file_path in locks:
            if locks[file_path]["team_id"] == team_id:
                del locks[file_path]
                cls._save_locks(locks)
                return True
        
        return False
    
    @classmethod
    def is_locked(cls, file_path: str) -> Optional[str]:
        """
        Check if a file is locked
        
        Args:
            file_path: Path to check
            
        Returns:
            Optional[str]: Team ID holding the lock, or None if not locked
        """
        locks = cls._load_locks()
        
        if file_path in locks:
            lock_info = locks[file_path]
            lock_time = datetime.fromisoformat(lock_info["timestamp"])
            
            # Check if lock is expired
            if datetime.now() - lock_time > timedelta(seconds=cls.LOCK_TIMEOUT):
                # Expired lock, clean it up
                del locks[file_path]
                cls._save_locks(locks)
                return None
            
            return lock_info["team_id"]
        
        return None
    
    @classmethod
    def clear_team_locks(cls, team_id: str) -> int:
        """
        Clear all locks held by a team
        
        Args:
            team_id: Team ID whose locks to clear
            
        Returns:
            int: Number of locks cleared
        """
        locks = cls._load_locks()
        cleared = 0
        
        for file_path in list(locks.keys()):
            if locks[file_path]["team_id"] == team_id:
                del locks[file_path]
                cleared += 1
        
        if cleared > 0:
            cls._save_locks(locks)
        
        return cleared
    
    @classmethod
    def get_all_locks(cls) -> Dict[str, Any]:
        """Get all current locks (for debugging)"""
        locks = cls._load_locks()
        
        # Add expiry status
        current_time = datetime.now()
        for path, lock_info in locks.items():
            lock_time = datetime.fromisoformat(lock_info["timestamp"])
            remaining = cls.LOCK_TIMEOUT - (current_time - lock_time).total_seconds()
            lock_info["expires_in"] = max(0, int(remaining))
        
        return locks


# Example usage in team agents:
"""
from file_lock_manager import FileLockManager

# In team agent code:
if FileLockManager.acquire_lock("src/constants.py", "team1"):
    try:
        # Modify the file
        edit_file("src/constants.py", ...)
    finally:
        FileLockManager.release_lock("src/constants.py", "team1")
else:
    # Could not acquire lock
    team_context["messages"].append("Could not acquire lock on src/constants.py")
"""