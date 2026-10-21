"""Novel-local production launcher."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent / 'src'))
from novel_creator.cli import main
raise SystemExit(main())
