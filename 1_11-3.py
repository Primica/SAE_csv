import csv


class CsvTransactionProcessor:
    client_id_counter = 1
    product_id_counter = 1
    order_id_counter = 1

    """
    Méthodes pour générer un identifiant client unique, en incrémentant un compteur de clients / produit / commandes.
    """
    @staticmethod
    def generate_client_id():
        id = f"CL{CsvTransactionProcessor.client_id_counter:06d}"
        CsvTransactionProcessor.client_id_counter += 1
        return id

    @staticmethod
    def generate_product_id():
        id = f"PR{CsvTransactionProcessor.product_id_counter:06d}"
        CsvTransactionProcessor.product_id_counter += 1
        return id

    @staticmethod
    def generate_order_id():
        id = f"OR{CsvTransactionProcessor.order_id_counter:06d}"
        CsvTransactionProcessor.order_id_counter += 1
        return id

    """
    Charge les transactions à partir d'un fichier CSV.

    Args:
        file_path (str): Le chemin du fichier CSV à charger.

    Returns:
        list: Une liste de dictionnaires représentant les transactions.
    """
    @staticmethod
    def load_transactions(file_path):
        with open(file_path, mode="r", encoding="utf-8-sig") as fichier:
            lecteur = csv.reader(fichier, delimiter=',')
            noms_colonnes = next(lecteur)
            transactions = []
            for ligne in lecteur:
                transaction = {
                    "raison": ligne[0],
                    "adresse_1": ligne[1],
                    "adresses_2": ligne[2],
                    "catégorie": ligne[3],
                    "produit": ligne[4],
                    "quantite": int(ligne[5]),
                    "prix_unitaire": ligne[6],
                    "date": ligne[7]
                }
                transactions.append(transaction)
        return transactions


    """
    Charge les commandes à partir d'un fichier CSV.

    Args:
        file_path (str): Le chemin du fichier CSV à charger.

    Returns:
        list: Une liste de dictionnaires représentant les commandes.
    """
    @staticmethod
    def load_commandes(file_path):
        with open(file_path, mode="r", encoding="utf-8-sig") as fichier:
            lecteur = csv.reader(fichier, delimiter=',')
            noms_colonnes = next(lecteur)
            commandes = []
            for ligne in lecteur:
                commande = {
                    "identifiant_commande": ligne[0],
                    "identifiant_client": ligne[1],
                    "identifiant_produit": ligne[2],
                    "quantite": ligne[3],
                    "prix_unitaire": ligne[4],
                    "date": ligne[5]
                }
                commandes.append(commande)
        return commandes

    """
    Construit de nouveaux fichiers CSV à partir des transactions fournies.

    Cette méthode crée trois fichiers CSV : clients.csv, produits.csv et commandes.csv.
    - clients.csv contient les informations sur les clients.
    - produits.csv contient les informations sur les produits.
    - commandes.csv contient les informations sur les commandes.

    Args:
        transactions (list): Une liste de dictionnaires représentant les transactions. 

    Raises:
        KeyError: Si une clé requise est manquante dans une transaction.
    """
    @staticmethod
    def construct_new_files_from_transactions(transactions):
        clients = {}
        with open('csv/clients.csv', mode='w', encoding='utf-8-sig', newline='') as fichier_clients:
            champs_clients = ["identifiant_client", "raison_sociale", "derniere_adresse_connue"]
            writer_clients = csv.DictWriter(fichier_clients, fieldnames=champs_clients)
            writer_clients.writeheader()

            for transaction in transactions:
                client = transaction["raison"]
                if client not in clients:
                    client_id = CsvTransactionProcessor.generate_client_id()
                    clients[client] = client_id
                    writer_clients.writerow({
                        "identifiant_client": client_id,
                        "raison_sociale": client,
                        "derniere_adresse_connue": transaction["adresse_1"] + " " + transaction["adresses_2"]
                    })

        produits = {}
        with open('csv/produits.csv', mode='w', encoding='utf-8-sig', newline='') as fichier_produits:
            champs_produits = ["identifiant_produit", "libelle", "catégorie", "dernier_prix_connu"]
            writer_produits = csv.DictWriter(fichier_produits, fieldnames=champs_produits)
            writer_produits.writeheader()

            for transaction in transactions:
                produit = transaction["produit"]
                if produit not in produits:
                    product_id = CsvTransactionProcessor.generate_product_id()
                    produits[produit] = product_id
                    writer_produits.writerow({
                        "identifiant_produit": product_id,
                        "libelle": produit,
                        "catégorie": transaction["catégorie"],
                        "dernier_prix_connu": transaction["prix_unitaire"]
                    })

        with open('csv/commandes.csv', mode='w', encoding='utf-8-sig', newline='') as fichier_commandes:
            champs_commandes = ["identifiant_commande", "identifiant_client", "identifiant_produit", "quantite",
                                "prix_unitaire", "date"]
            writer_commandes = csv.DictWriter(fichier_commandes, fieldnames=champs_commandes)
            writer_commandes.writeheader()

            for transaction in transactions:
                writer_commandes.writerow({
                    "identifiant_commande": CsvTransactionProcessor.generate_order_id(),
                    "identifiant_client": clients[transaction["raison"]],
                    "identifiant_produit": produits[transaction["produit"]],
                    "quantite": transaction["quantite"],
                    "prix_unitaire": transaction["prix_unitaire"],
                    "date": transaction["date"]
                })

    """
    Calcule le nombre de commandes passées par un client spécifique.

    Args:
        commandes (list): Liste de dictionnaires représentant les commandes.
        client_id (int): Identifiant du client.

    Returns:
        int: Nombre de commandes passées par le client.
    """
    @staticmethod
    def get_order_count_by_client(commandes, client_id):
        return sum(1 for commande in commandes if commande["identifiant_client"] == client_id)

    """
    Calcule la moyenne des commandes par client.

    Cette méthode prend une liste de commandes et calcule le nombre moyen de commandes par client.

    Args:
        commandes (list): Une liste de dictionnaires représentant les commandes. Chaque dictionnaire doit contenir une clé "identifiant_client" correspondant à l'identifiant du client.

    Returns:
        float: Le nombre moyen de commandes par client. Retourne 0 si la liste des commandes est vide.
    """
    @staticmethod
    def calculate_average_orders(commandes):
        client_order_counts = {}
        for commande in commandes:
            client_id = commande["identifiant_client"]
            client_order_counts[client_id] = client_order_counts.get(client_id, 0) + 1

        total_orders = sum(client_order_counts.values())  
        total_clients = len(client_order_counts)  
        return total_orders / total_clients if total_clients > 0 else 0

    """
    Calcule le nombre maximum de commandes passées par un client.

    Args:
        commandes (list): Une liste de dictionnaires représentant les commandes. 
                          Chaque dictionnaire doit contenir une clé "identifiant_client".

    Returns:
        tuple: Un tuple contenant l'identifiant du client avec le plus de commandes 
               et le nombre de commandes passées par ce client. Si aucune commande 
               n'est trouvée, retourne (None, 0).
    """
    @staticmethod
    def calculate_max_orders(commandes):
        client_order_counts = {}
        for commande in commandes:
            client_id = commande["identifiant_client"]
            client_order_counts[client_id] = client_order_counts.get(client_id, 0) + 1

        max_client = max(client_order_counts, key=client_order_counts.get, default=None)
        max_orders = client_order_counts[max_client] if max_client else 0
        return max_client, max_orders
    

    """
    Calcule le nombre maximum de produits par catégorie à partir des transactions.

    Args:
        transactions (list): Une liste de dictionnaires représentant les transactions. 
                             Chaque dictionnaire doit contenir les clés "catégorie" et "quantite".

    Returns:
        tuple: Une paire contenant la catégorie avec le plus grand nombre de produits et le nombre de produits dans cette catégorie.
               Si aucune transaction n'est fournie, retourne (None, 0).
    """
    @staticmethod
    def calculate_max_products_by_category(transactions):
        category_product_counts = {}
        for transaction in transactions:
            category = transaction["catégorie"]
            category_product_counts[category] = category_product_counts.get(category, 0) + transaction["quantite"]

        max_category = max(category_product_counts, key=category_product_counts.get, default=None)
        max_products = category_product_counts[max_category] if max_category else 0
        return max_category, max_products

def calculate_average_products_per_category(file_path):
    category_product_counts = {}
    category_transaction_counts = {}

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            category = row['catégorie']
            quantity = int(row['quantité'])

            if category not in category_product_counts:
                category_product_counts[category] = 0
                category_transaction_counts[category] = 0

            category_product_counts[category] += quantity
            category_transaction_counts[category] += 1

    category_averages = {category: category_product_counts[category] / category_transaction_counts[category]
                         for category in category_product_counts}

    return category_averages


if __name__ == "__main__":
    transactions = CsvTransactionProcessor.load_transactions("transactions.csv")
    if transactions:
        CsvTransactionProcessor.construct_new_files_from_transactions(transactions)

    commandes = CsvTransactionProcessor.load_commandes("csv/commandes.csv")

    average_orders = CsvTransactionProcessor.calculate_average_orders(commandes)
    print(f"Moyenne des commandes par client : {average_orders}")

    max_client, max_orders = CsvTransactionProcessor.calculate_max_orders(commandes)
    print(f"Client avec le maximum de commandes : {max_client} ({max_orders} commandes)")

    max_category, max_products = CsvTransactionProcessor.calculate_max_products_by_category(transactions)
    print(f"Catégorie avec le maximum de produits commandés : {max_category} ({max_products} produits)")

    print(calculate_average_products_per_category("transactions.csv"))