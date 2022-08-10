from logging import exception
from booking.searching import Searching

try:
    inst = Searching(test=False)
    # print('\ntest')
    # sys.stdout.flush()
    inst.land_first_page()
    # import pdb; pdb.set_trace()
    inst.first_search(date=1)
    inst.search()
except Exception as e:
    if 'in PATH' in str(e):
        print(
            'You are trying to run the bot from comand line\n'
            'Please add your selenium drivers to PATH:\n'
            'Windows: \n'
            '   set PATH=%PATH%;C:path-to-your-folder\n'
            'Linux: \n'
            '   PATH=$PATH:/path/to/your/folder\n'
        )
    else:
        raise

# from booking.filtering import Filtering
# inst = Searching()
# filt = Filtering(inst)
# filt.bingo()