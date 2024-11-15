import requests
import json

# Informations d'authentification OneSignal
API_KEY = "os_v2_app_xjfnsbamhvhltn7wgx3kg3aysntdeb7yvgee2p4bmig7r4myuiavmvjheg5ikmy4qjp5zjthui6oxsv3wvfsavd4a3ev23wywita63q"
APP_ID = "ba4ad904-0c3d-4eb9-b7f6-35f6a36c1893"

# URL de l'API OneSignal
url = "https://onesignal.com/api/v1/notifications"

# Détails de la notification
notification_data = {
    "app_id": APP_ID,
    "included_segments": ["Total Subscriptions"],  # Envoie à tous les abonnés
    "headings": {"en": "Titre de la notification"},
    "contents": {"en": "Contenu de la notification"},
    "url": "https://votre-site.com"  # URL vers laquelle rediriger les utilisateurs
}

# En-têtes pour la requête
headers = {
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": f"Basic {API_KEY}"
}

# Envoi de la requête POST
response = requests.post(url, headers=headers, data=json.dumps(notification_data))

# Vérification de la réponse
if response.status_code == 200:
    print("Notification envoyée avec succès !")
    print("Réponse de l'API:", response.json())
else:
    print("Erreur lors de l'envoi de la notification.")
    print("Code de statut :", response.status_code)
    print("Réponse de l'API :", response.text)
