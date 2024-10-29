import logging
import sys

from character_dump.dump import CharacterDump

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

print('Deseja apagar as midias existentes? S/N')
apagar_midia_str = input()

characterDump = CharacterDump()
characterDump.doDump(total_personagens=10000, 
					 apagar_midia=(apagar_midia_str == "S" or apagar_midia_str == "s"))