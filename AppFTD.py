
import multiprocessing

from app import main
from app.core.common  import is_win

if __name__ == '__main__':
    if is_win():
        multiprocessing.freeze_support()
    main()
