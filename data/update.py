from ipca_fetch_all import update_db

def update_all(dat):
    update_db('ipca_mom.csv', 'mom', dat)
    update_db('ipca_peso.csv', 'peso', dat)
