#!/usr/bin/env python3
"""
DNA Methodology Guide 파일들을 하나로 합치는 스크립트
"""
import os
from pathlib import Path
from datetime import datetime

# 설정
SOURCE_DIR = Path("/Users/jason/Projects/spark-claude/docs/DNA_Methodology_v4.0_Guide")
OUTPUT_FILE = SOURCE_DIR / "DNA_ALL_GUIDES_MERGED.md"

# *.guide.md 또는 *_guide.md 패턴 파일 찾기
guide_files = sorted(SOURCE_DIR.glob("*_guide.md"))

print(f"Found {len(guide_files)} guide files:")
for f in guide_files:
    print(f"  - {f.name}")

# 합치기
with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
    # 헤더 작성
    outfile.write("# DNA Methodology v4.0 - All Guides (Merged)\n\n")
    outfile.write(f"**생성일**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    outfile.write(f"**포함된 파일**: {len(guide_files)}개\n\n")
    outfile.write("---\n\n")
    
    # 목차 작성
    outfile.write("## 📚 목차\n\n")
    for idx, guide_file in enumerate(guide_files, 1):
        outfile.write(f"{idx}. [{guide_file.name}](#{guide_file.stem})\n")
    outfile.write("\n---\n\n")
    
    # 각 파일 내용 추가
    for idx, guide_file in enumerate(guide_files, 1):
        print(f"\nProcessing {idx}/{len(guide_files)}: {guide_file.name}")
        
        with open(guide_file, 'r', encoding='utf-8') as infile:
            content = infile.read()
        
        # 파일 구분자 추가
        outfile.write(f"\n\n{'='*80}\n")
        outfile.write(f"# 📄 {idx}. {guide_file.name}\n")
        outfile.write(f"{'='*80}\n\n")
        
        # 원본 내용 추가
        outfile.write(content)
        
        # 파일 끝 표시
        outfile.write(f"\n\n{'='*80}\n")
        outfile.write(f"# End of {guide_file.name}\n")
        outfile.write(f"{'='*80}\n\n")

print(f"\n✅ 완료! 결과 파일: {OUTPUT_FILE}")
print(f"   총 {len(guide_files)}개 파일이 병합되었습니다.")
