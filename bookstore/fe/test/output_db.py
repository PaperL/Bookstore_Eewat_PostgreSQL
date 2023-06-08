from be.model.database import getDatabase
from fe.access import BookTable

session = getDatabase()
books = BookTable.get_book_info(session, 0, 0)

with open('output.txt', 'w') as f:
    for b in books:
        b_dict = b.__dict__.copy()
        # b_dict.pop('_sa_instance_state', None)
        b_dict.pop('pictures', None)
        b_dict.pop('author_intro', None)
        b_dict.pop('book_intro', None)
        # b_dict.pop('content', None)
        
        for k, v in b_dict.items():
            f.write(f'{k}: {v}\n')
        f.write('\n\n')

session.close()
