# TkLearn Studio - Édition Professionnelle

TkLearn Studio est un **Environnement de Développement Intégré (IDE)** autonome et visuellement saisissant, bâti à 100% en Python natif avec `tkinter`.

Il a été conçu spécifiquement pour l'apprentissage guidé et le prototypage rapide d'interfaces graphiques (GUI). Il permet aux apprenants et développeurs de rédiger du code Tkinter classique, puis de **prévisualiser instantanément l'interface générée** à l'intérieur même du studio, sans qu'aucune fenêtre externe ne vienne polluer l'écran. 

C'est un véritable bac à sable de code interactif, conçu avec l'esthétique et l'ergonomie des éditeurs de code professionnels modernes tels que `Visual Studio Code` et inspiré par la fluidité des interfaces IA réçentes comme `Gemini`.

---

## Fonctionnalités Majeures

### 1. Esthétique Premium (Thème Dark+ / Antigravity)
L'interface utilisateur a été raffinée pour repousser les limites de Tkinter originel :
- **Color Scheme unifié :** Tons sombres neutres professionnels (`#1e1e1e`, `#2d2d30`, `#333333`) avec des textes gris doux pour le confort visuel.
- **Activity Bar Verticale :** Une barre d'action élégante à gauche de l'écran (avec indicateurs actifs bleus) pour invoquer instantanément l'explorateur ou l'assistant IA.
- **Scrollbars Invisibles / Sombres :** Des barres de défilement plates, réactives au survol, qui se fondent parfaitement dans le décor.
- **Status Bar Intégrée :** Une barre d'état inférieure bleue affichant le fichier actif, l'état d'exécution, et la position dynamique du curseur.

### 2. L'Éditeur Intelligent (`CodeEditor`)
Fini le simple bloc-notes. L'éditeur agit comme un IDE complet :
- **Coloration Syntaxique Live (Syntax Highlighting) :** Les mots-clés (`def`, `class`, `import`), fonctions natives, chaînes et nombres prennent couleur sans "lag" grâce aux timers Tcl optimisés.
- **Numérotation des Lignes Dynamique :** Un canvas en bordure qui suit et dessine le numéro de chaque ligne, totalement synchronisé avec le scrolling.
- **Typage Intelligent (Smart Typing) :**
  - Auto-fermeture instantanée de vos guillemets `""`, parenthèses `()`, et crochets `[]`.
  - **Smart Indentation :** L'appui sur *Entrée* reproduit le niveau d'indentation précédent, et ajoute automatiquement 4 espaces après un block conditionnel ou de fonction (`:`).

### 3. Assistant Code IA Intégré (Panneau Latéral)
TkLearn Studio embarque nativement une surcouche d'assistance générative alimentée par l'API **Mistral**.
- **Interface Chat Fluide :** Plus de popup gênante. L'assistant vit dans un panneau latéral coulissant, avec une page d'accueil centrée style "Gemini" et un historique de bulles de chat (scrollable, hauteur automatique).
- **Sélecteur de Modèle Dynamique :** Le bas du panneau vous permet de choisir la complexité du réseau utilisé (`small`, `medium`, `large`).
- **Prompt to UI Asynchrone :** Demandez ("Crée moi une horloge digitale"), l'IA génère les composants et les injecte magiquement dans l'éditeur sans jamais bloquer ou "freezer" l'application (Multi-threading). 

### 4. Code Executor & Sandbox ("Preview Live")
Il s'agit du cœur magique de cette application. En temps normal, la fonction Python `exec()` dans Tkinter est risquée et génère de multiples fenêtres. Mais notre `CodeExecutor` va :
- **Moquer (Mocking) dynamiquement Tkinter :** N'importe quel code appelant `tk.Tk()` instanciera en réalité de manière transparente notre widget de prévisualisation interne (`PreviewFrame`).
- **Bloquer les mainloops infinis :** Les appels `root.mainloop()` rédigés par les élèves sont annihilés/interceptés silencieusement pour empêcher le studio de planter.
- **Captures Clavier Dédiées :** Vous pouvez coder un vrai jeu fléché (ex: Snake) ! Le studio intercepte vos appels `bind()` et transfère le **Focus Clavier** directement à la frame de prévisualisation cliquable. Autorisant des applications 100% interactives.
- **Redirection de la Boucle d'Événements :** Les `after()` et callback asynchrones du code testé sont wrappées pour ne pas faire crasher l'application mère en cas d'erreur.
- **Rediriger le Terminal :** Les sorties standard (`print()`) et les `Tracebacks` d'erreur s'affichent proprement dans la Console grisée intégrée en bas, colorisées selon leur sévérité.

### 5. Inspecteur d'Arborescence Temps-Réel (`WidgetInspector`)
La prévisualisation est scrutée par un puissant outil pédagogique :
- Après l'exécution d'un code, le **Widget Inspector** vient scanner le sous-arbre graphique généré par votre script.
- Il construit dynamiquement un `Treeview` qui montre exactement "qui est dans quoi". Idéal pour apprendre ou déboguer le Layout Manager (`pack`, `grid`). 

### 6. Apprentissage Basé sur des Leçons
Un catalogue de leçons cliquables (L'essentiel, Options Multiples, Grilles, Canvas, Bindings) est embarqué.
Toutes nos leçons sont formatées avec la pure architecture classique `root = tk.Tk(); root.mainloop()`. Elles sont pensées pour pouvoir être **copiées et exécutées hors du studio** sans aucune modification, tout en tournant parfaitement à l'intérieur.

---

## Architecture du Code Source

L'application est découpée intelligemment (Séparation Interface vs Logique) :

```text
📁 tklearn_studio/
├── 📄 main.py                   (Point d'Entrée Central, Conteneurs PanedWindow)
└── 📁 src/
    ├── 📁 core/                 (Moteurs Logiques "Invisibles")
    │   ├── 📄 executor.py       (Magie du Mocking Tk, Focus Clavier virtuel, Boucle & Exec)
    │   ├── 📄 ai_client.py      (Serveur d'API multi-thread pour les modèles LLM configurables)
    │   ├── 📄 file_manager.py   (Dialogues OS: Ouvertures, Sauvegardes .py)
    │   └── 📄 lesson_loader.py  (Catalogue statique de cours Tkinter prêt-à-injecter)
    │
    └── 📁 ui/                   (Le Rendu / Les Composants Visuels)
        ├── 📄 editor.py         (Editeur de texte sur-vitaminé, Indentation IA)
        ├── 📄 preview.py        (Frame Cliquable réceptacle du code injecté)
        ├── 📄 inspector.py      (Arbre "ttk.Treeview" explorateur de widgets construits)
        ├── 📄 console.py        (Terminal logger colorisé de sorties standards et d'erreurs)
        ├── 📄 ai_assistant.py   (Panneau latéral de discussion, Sélecteur LLM, Home Screen)
        ├── 📄 status_bar.py     (Pied-de-page informatif dynamique, Ln/Col tracker)
        ├── 📄 menus.py          (AppMenu supérieur: Fichiers, Outils, Raccourcis OS)
        └── 📄 theme.py          (Unico-déclaration Constantes Couleurs, Polices et Scrollbars)
```

---

## Prérequis et Installation

**Aucune installation tierce externe n'est requise !**
TkLearn Studio se repose exclusivement sur la Standard Library de Python 3 (`tkinter`, `urllib`, `threading`, `sys`, `re`). **Aucun `pip install` n'est nécessaire**.

> **Note IA :** Pour utiliser l'assistant génératif, une Clé API valide pour le fournisseur choisi devra exister dans vos variables d'environnement (`MISTRAL_API_KEY`). Si ce n'est pas le cas, l'assistant vous reverra une erreur claire mais l'IDE continuera de fonctionner parfaitement.

## Exécution

Ouvrez un terminal, placez-vous à la racine du projet et exécutez simplement :

```bash
python main.py
```

> *(Astuce : Appuyez n'importe quand sur la touche **F5** pour exécuter instantanément le code de l'éditeur sur la droite !).*
