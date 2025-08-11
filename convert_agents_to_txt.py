#!/usr/bin/env python3
"""
SPARK 에이전트 MD 파일을 TXT로 변환하는 스크립트
Gemini가 MD 파일을 잘 읽지 못하는 문제 해결용
"""

import os
import shutil
from pathlib import Path

def convert_md_to_txt(agents_dir):
    """
    agents 디렉토리의 모든 .md 파일을 .txt로 변환
    """
    agents_path = Path(agents_dir)
    
    if not agents_path.exists():
        print(f"❌ 경로를 찾을 수 없습니다: {agents_dir}")
        return
    
    # 변환된 파일을 저장할 디렉토리 생성
    output_dir = agents_path.parent / "agents_txt"
    output_dir.mkdir(exist_ok=True)
    
    # .md 파일 찾기
    md_files = list(agents_path.glob("*.md"))
    
    if not md_files:
        print(f"⚠️ {agents_dir}에 .md 파일이 없습니다.")
        return
    
    print(f"📁 출력 디렉토리: {output_dir}")
    print(f"📝 {len(md_files)}개의 .md 파일을 변환합니다...\n")
    
    converted_count = 0
    for md_file in md_files:
        try:
            # .txt 파일 경로 생성
            txt_filename = md_file.stem + ".txt"
            txt_path = output_dir / txt_filename
            
            # 파일 내용 읽기
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # .txt 파일로 저장
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {md_file.name} → {txt_filename}")
            converted_count += 1
            
        except Exception as e:
            print(f"❌ {md_file.name} 변환 실패: {e}")
    
    print(f"\n🎉 변환 완료! {converted_count}/{len(md_files)} 파일이 성공적으로 변환되었습니다.")
    print(f"📂 변환된 파일 위치: {output_dir}")
    
    # 하나의 통합 파일도 자동 생성
    print("\n📚 통합 파일을 생성합니다...")
    if True:
        combined_path = output_dir / "all_agents_combined.txt"
        with open(combined_path, 'w', encoding='utf-8') as combined:
            combined.write("=" * 80 + "\n")
            combined.write("SPARK v3.5 - 모든 에이전트 정의 통합 파일\n")
            combined.write("=" * 80 + "\n\n")
            
            for md_file in sorted(md_files):
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                combined.write(f"\n{'='*80}\n")
                combined.write(f"파일: {md_file.name}\n")
                combined.write(f"{'='*80}\n\n")
                combined.write(content)
                combined.write("\n\n")
        
        print(f"✅ 통합 파일 생성: {combined_path}")

if __name__ == "__main__":
    # SPARK 프로젝트의 agents 디렉토리 경로
    agents_directory = "/Users/jason/Projects/spark-claude/.claude/agents"
    
    print("🚀 SPARK 에이전트 MD → TXT 변환 스크립트")
    print("=" * 50)
    
    convert_md_to_txt(agents_directory)