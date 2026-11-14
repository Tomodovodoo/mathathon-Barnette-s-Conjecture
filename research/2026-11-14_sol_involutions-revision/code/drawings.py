import sys,json
from pathlib import Path
sys.dont_write_bytecode=True
root=Path.cwd();out=root/'research/2026-11-14_sol_involutions-revision'
sys.path.insert(0,str(root/'research/2026-11-14_opus_referee-involutions/code'))
src=(root/'research/2026-11-14_opus_referee-involutions/code/running.py').read_text()
src=src.replace("(HERE / 'out' / 'running.json')", "(Path(r'"+str(out)+"') / 'drawing-census.json')")
exec(compile(src,'referee-running-recheck','exec'),{'__file__':str(root/'research/2026-11-14_opus_referee-involutions/code/running.py'),'__name__':'__main__'})
