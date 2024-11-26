import csv


class CsvTransactionProcessor:
    client_id_counter = 1
    product_id_counter = 1
    order_id_counter = 1

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

    @staticmethod
    def get_order_count_by_client(commandes, client_id):
        return sum(1 for commande in commandes if commande["identifiant_client"] == client_id)



if __name__ == "__main__":
    transactions = CsvTransactionProcessor.load_transactions("transactions.csv")
    CsvTransactionProcessor.construct_new_files_from_transactions(transactions)

