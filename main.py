import logging
import sys

from character_dump.dump import CharacterDump

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

characterDump = CharacterDump()
characterDump.doDump()