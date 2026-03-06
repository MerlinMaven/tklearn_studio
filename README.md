#  TkLearn Studio - Édition Professionnelle

TkLearn Studio est un **Environnement de Développement Intégré (IDE)** autonome et visuellement saisissant, bâti à 100% en Python natif avec `tkinter`.

Il a été conçu spécifiquement pour l'apprentissage guidé et le prototypage rapide d'interfaces graphiques (GUI). Il permet aux apprenants et développeurs de rédiger du code Tkinter classique, puis de **prévisualiser instantanément l'interface générée** à l'intérieur même du studio, sans qu'aucune fenêtre externe ne vienne polluer l'écran. 

C'est un véritable bac à sable de code, conçu avec l'esthétique et l'ergonomie des éditeurs de code professionnels modernes tels que `Visual Studio Code`.

---

##  Fonctionnalités Majeures

###  1. Esthétique Premium (Thème Dark+ "VS Code")
L'interface utilisateur a été raffinée pour repousser les limites de Tkinter originel :
- **Colors Scheme unifié :** Tons `Dark/Grey` professionnels (`#1e1e1e`, `#2d2d30`, `#333333`).
- **Activity Bar Rétractable :** Une barre d'action élégante (hauteur fixe 35px, icônes réactives) située à gauche de l'écran pour invoquer les pannels secondaires.
- **Titres et En-têtes Épurés :** Polices `Segoe UI` modernes, séparateurs "borderless", et accents de couleur fins (comme le bandeau de prévisualisation `#007acc`).

###  2. L'Éditeur Intelligent (`CodeEditor`)
Fini le simple bloc-notes. Notre zone d'édition (`src/ui/editor.py`) agit comme un vrai IDE :
- **Coloration Syntaxique Live (Syntax Highlighting) :** Les mots-clés (`def`, `class`, `import`), fonctions natives (`print`), chaînes de caractères et nombres prennent doucement couleur à chaque frappe avec les teintes du thème "Dark+" de VS Code.
- **Numérotation des Lignes Dynamique :** Un canvas en bordure qui suit et dessine parfaitement le numéro de chaque ligne, totalement synchronisé avec le `Scrollbar`.
- **Typage Intelligent (Smart Typing) :**
  - Auto-fermeture instantanée de vos guillemets `""`, parenthèses `()`, et crochets `[]`.
  - **Smart Indentation :** La touche *Entrée* reproduit le niveau d'indentation de la ligne au-dessus. Encore mieux : après le caractère balise `:`, l'éditeur injecte magiquement une indentation de 4 espaces pour Python !

###  3. Assistant Code IA Propulsé par Mistral (`AIAssistantDialog`)
TkLearn Studio embarque nativement une surcouche d'assistance générative alimentée par **Mistral AI** (`mistral-small-latest`).
- **Prompt to UI :** Le bouton magique ✨ dans `l'Activity Bar` ouvre un dialog permettant à l'utilisateur de décrire en langage naturel ce qu'il souhaite coder (ex: *"Crée moi un Login Form avec Grid"*).
- **Asynchronisme :** La requête vers Mistral ne fige pas l'interface (Multi-threading).
- **Injection Directe :** Le code rendu par l'IA est nettoyé en arrière-plan et injecté automatiquement dans l'Éditeur, prêt à être exécuté par pression de la touche `[F5]`.

###  4. Exécuteur "Sandbox" par Interception (`CodeExecutor`)
Il s'agit du cœur magique de cette application. En temps normal, la fonction Python `exec()` dans Tkinter est risquée et génère de multiples fenêtres. Mais notre `CodeExecutor` va :
- **Moquer/Surcharger (Mocking) dynamiquement Tkinter :** N'importe quel code élève appelant `tk.Tk()` instanciera en réalité de manière transparente notre widget de prévisualisation interne (`PreviewFrame`).
- **Bloquer les plantages de fenêtre racine :** Les appels natifs `root.mainloop()` (ou d'injection infinie) rédigés par les élèves sont annihilés/interceptés pour empêcher le studio maître de planter.
- **Rediriger le Terminal :** Les sorties standard (`print("Mon Texte")`) de l'utilisateur ne sont jamais perdues, elles sont interceptées et copiées en direct dans la **Console Intégrée** du bas de l'écran.
- **Coloration d'Erreurs :** En cas d'erreur de saisie élève (`Traceback`), l'écran Tkinter ne gèle pas. L'erreur est capturée subtilement et affichée dans le terminal interne en rouge/vert pour un débug facile.

###  5. Inspecteur d'Arborescence Temps-Réel (`WidgetInspector`)
La prévisualisation n'est pas qu'un écran vide, elle est scrutée par un outil pédagogique :
- Après chaque exécution de code, le **Widget Inspector** (panneau latéral façon explorateur de fichiers) vient **scanner récursivement le DOM** Python de la vue finale du Tkinter généré.
- Il construit dynamiquement le **Widget Tree** (l'arbre graphique) afin de montrer visuellement à l'étudiant comment s'empilent ses éléments, avec des icônes déductives pour les Containers ( `Frame`), les Actions ( `Button`) et les Textes ( `Label`).

###  6. Gestionnaire Fichiers et Tutoriels Intégrés (`AppMenu`)
- Sauvegarde locale ultra-rapide grâce à `Ctrl+S`, ouverture (`Ctrl+O`) ou fonction de type `Enregistrer Sous...`.
- Apprentissage pas-à-pas grâce au menu contextuel supérieur `Leçons`, qui pousse dynamiquement du code didactique d'exemple dans votre espace éditeur pour vous en faire comprendre le principe.

---

##  Architecture du Code Source
Le projet adhère à d'excellentes normes "Clean Code", avec séparation logique (MVC-like) en modules distincts, facilitant sa compréhension métier :

```text
📁 tklearn_studio/
├── 📄 main.py                   (Point d'Entrée Central, orchestration globale UI Container)
└── 📁 src/
    ├── 📁 core/                 (La Logique Métier "Invisible")
    │   ├── 📄 executor.py       (Magie du Mocking Tk, Redirection, Protection `exec`, Tracebacks)
    │   ├── 📄 ai_client.py      (Moteur d'API local `urllib` & Requêtes Mistral asynchrones)
    │   └── 📄 file_manager.py   (Dialogues OS : Sauvegardes, Ouvertures de .py)
    │
    └── 📁 ui/                   (Le Rendu Graphique / Composants Visuels)
        ├── 📄 editor.py         (Éditeur riche intelligent couplé au Canvas LineNumbering)
        ├── 📄 preview.py        (Frame-réceptacle dédiée au faux "root.mainloop" élève)
        ├── 📄 inspector.py      (Arbre "ttk.Treeview" clam-themed d'exploration Widgets)
        ├── 📄 console.py        (Faux terminal read-only `state="disabled"` pour le débuggage)
        ├── 📄 ai_assistant.py   (Interface popup IA de prompting asynchrone)
        └── 📄 menus.py          (Génération standard de la menubar et injection pédagogique)
```

---

##  Guide d'Installation et Exécution

**Aucun Setup externe n'est requis !**
TkLearn Studio se repose exclusivement sur la Standard Library de Python 3 (built-in modules `tkinter`, `urllib`, `threading`, `sys`, `re`). Il n'y a **aucun `pip install`** ni dépendance tierce complexe à réaliser.

Exécutez simplement le point d'entrée depuis la racine de votre projet :
```bash
python tklearn_studio/main.py
```
> *(Astuce : Depuis l'application, appuyez n'importe quand sur la touche **F5** pour propulser et compiler votre code vers la zone droite !).*
