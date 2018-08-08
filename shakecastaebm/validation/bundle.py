from . import shakecast
from . import workbook
from . import damping
from . import demand

def main():
    demand.main()
    workbook.main()
    shakecast.main()
    damping.main()

if __name__ == '__main__':
    main()
