import sys
from pathlib import Path
sys.dont_write_bytecode=True
root=Path.cwd();out=root/'research/2026-11-14_sol_involutions-revision'
here=root/'research/2026-11-14_opus_referee-involutions/code'
sys.path.insert(0,str(here));src=(here/'compare_running.py').read_text()
src=src.replace("(HERE / 'out' / 'compare-running.json')", "(Path(r'"+str(out)+"') / 'table-check.json')")
exec(compile(src,'referee-table-recheck','exec'),{'__file__':str(here/'compare_running.py'),'__name__':'__main__'})
