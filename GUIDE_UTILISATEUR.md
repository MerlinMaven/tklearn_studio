#  TkLearn Studio - Guide Utilisateur Complet

Bienvenue dans le manuel d'utilisation officiel de **TkLearn Studio**, l'Environnement de Développement Intégré (IDE) pensé pour l'apprentissage, la conception et le prototypage d'interfaces graphiques (GUI) en Python avec **Tkinter**.

Ce document vous guide à travers toutes les fonctionnalités de l'application, étape par étape, pour transformer un développeur débutant en un véritable expert de la conception d'interfaces.

---

##  Sommaire
1. [Qu'est-ce que TkLearn Studio ?](#1-quest-ce-que-tklearn-studio-)
2. [Interface Principale (Vue d'ensemble)](#2-interface-principale-vue-densemble)
3. [L'Éditeur de Code Intelligent](#3-léditeur-de-code-intelligent)
4. [La Prévisualisation en Temps Réel](#4-la-prévisualisation-en-temps-réel)
5. [L'Assistant Code IA (Générateur Mistral)](#5-lassistant-code-ia-générateur-mistral)
6. [L'Inspecteur de Widgets (DOM Explorer)](#6-linspecteur-de-widgets-dom-explorer)
7. [Catalogue de Leçons Interactives](#7-catalogue-de-leçons-interactives)
8. [Astuces et Raccourcis Claviers](#8-astuces-et-raccourcis-claviers)

---

## 1. Qu'est-ce que TkLearn Studio ?

Historiquement, apprendre Tkinter impliquait d'écrire du code dans un bloc-notes ou un IDE externe (comme VS Code, PyCharm), d'exécuter un terminal, et de voir une nouvelle fenêtre apparaître. S'il y avait une erreur, il fallait fermer la fenêtre, lire le terminal, corriger le code, et relancer. 

**TkLearn Studio résout ce problème.** C'est une application tout-en-un où :
- Le code que vous tapez s'exécute **à l'intérieur** même du logiciel, de manière sécurisée.
- Toute erreur est formatée en rouge dans une console internet, sans jamais faire crasher le logiciel.
- Les blocs, layout et design sont inspectables instantanément pour comprendre *"pourquoi mon bouton ne s'affiche pas correctement ?"*.

---

## 2. Interface Principale (Vue d'ensemble)

Lorsque vous ouvrez TkLearn Studio (`python main.py`), l'interface se divise en 5 zones majeures (Thème sombre façon Visual Studio Code) :

1. **La Barre de Menus (En haut) :** Permet de charger des fichiers, sauvegarder votre progression, exécuter le code ou charger des *Leçons* interactives.
2. **L'Activity Bar (Tout à gauche) :** La barre ultra-compacte contenant deux icônes :
   - 📁 **Dossier :** Affiche ou masque *l'Inspecteur d'Interface*.
   - ✨ **Étoiles :** Ouvre *l'Assistant IA Mistral*.
3. **L'Éditeur de Code Centrale :** Zone centrale textuelle où vous rédigez votre script Python.
4. **La Prévisualisation (À droite) :** La "Sandbox". C'est ici que votre code *prend vie*.
5. **Le Terminal & Sortie (En bas) :** Affiche vos `print()` ou vos erreurs (Traceback).

Les cloisons (barres grises verticales) entre l'Inspecteur, l'Éditeur et la zone de Prévisualisation sont **redimensionnables**. Cliquez-glissez pour ajuster la taille de vos panneaux !

---

## 3. L'Éditeur de Code Intelligent

L'éditeur central n'est pas un simple champ de texte, il assiste votre frappe :

- **Coloration Syntaxique Live :** Les fonctions comme `def`, `class`, `print` ou les variables apparaissent avec des couleurs distinctes (Thème Dark+) pour rendre le code digeste.
- **Numérotation des lignes :** Essentielle pour repérer facilement les erreurs annoncées par la console.
- **Indentation Automatique :** Appuyer sur `Entrée` après le symbole `:` (deux-points) va automatiquement indenter la ligne suivante de 4 espaces (Standard Python).
- **Auto-Fermeture :** Ouvrez une parenthèse `(`, un crochet `[`, ou un guillemet `"`, et le logiciel fermera automatiquement son homologue `)`, `]`, `"`.

---

## 4. La Prévisualisation en Temps Réel

Sous le capot, l'Éxecuteur (`CodeExecutor`) effectue une magie complexe appelée **"Mocking"** :

- Vous n'avez pas de questions à vous poser. Écrivez votre code EXACTEMENT comme dans les tutoriels normaux :
  ```python
  import tkinter as tk
  root = tk.Tk()
  tk.Label(root, text="Mon Texte").pack()
  root.mainloop()
  ```
- L'éditeur va subrepticement intercepter `tk.Tk()` et empêcher `root.mainloop()` de créer une seconde application. Il va injecter vos widgets directement dans la **Zone de Prévisualisation** de droite au sein de notre architecture parent.
- **Exécution :** Vous pouvez déclencher le rafraîchissement visuel à tout moment soit en allant dans `Menu > Exécution > Exécuter le code`, soit en pressant la touche magique **`F5`**.

---

## 5. L'Assistant Code IA (Générateur Mistral)

Bloqué(e) sur la syntaxe d'un formulaire ou en manque d'inspiration ? L'IA générative connectée nativement à **Mistral AI** peut vous pondre du code parfait en 5 secondes.

1. Cliquez sur l'icône **✨ (Étoiles)** située dans la barre de gauche (*Activity Bar*).
2. Une élégante boîte de dialogue s'ouvre.
3. Rédigez en français (ou anglais) ce que vous souhaitez. *Exemple : "Crée une calculatrice qui occupe tout l'écran avec une grille colorée."*
4. Appuyez sur **Générer le code**.
5. L'IA réfléchit (sans bloquer le logiciel) et la console vous informe de son statut.
6. Une fois prêt, le code magistral est **injecté automatiquement** dans votre éditeur ! Vous n'avez plus qu'à appuyer sur `F5` pour l'admirer.

*(Note : Requiert une connexion internet valide. La clé API est déjà encodée sécuritairement dans le source).*

---

## 6. L'Inspecteur de Widgets (DOM Explorer)

C'est l'outil pédagogique par excellence (situé dans le volet le plus à gauche).

*Comment sont rangés mes éléments Tkinter dans la mémoire ?*
Après chaque exécution (`F5`), l'application **scanne de manière récursive (profonde)** votre code Tkinter généré et dresse un arbre (TreeView) visuel avec des icônes :

- 📂 : Les frames et containers de base (`tk.Frame`, `tk.PanedWindow`).
- 📝 : Les éléments textuels passifs (`tk.Label`, `tk.Message`).
- 🔘 : Les actions cliquables (`tk.Button`, `tk.Radiobutton`, `tk.Checkbutton`).
- 🔤 : Les entrées de type formulaire (`tk.Entry`, `tk.Text`, `ttk.Combobox`).

Ceci permet à l'apprenant de parfaitement comprendre la hiérarchie parent > enfant (le Document Object Model) propre à Tkinter.

---

## 7. Catalogue de Leçons Interactives

Pas envie de lire la documentation officielle ? Apprenez Tkinter par la pratique.
Cliquez sur le menu supérieur **`Leçons`**, et choisissez parmi les exercices embarqués :

1. **Les Bases :** Apprenez le trio vital (Label, Entry, Button) avec interaction simple.
2. **Choix Multiples :** Apprenez que les Radiobuttons lient des `tk.IntVar()` entre eux.
3. **Mise en page :** Comprenez que pour construire des formulaires, c'est la fonction paramétrique `.grid(row=X, column=Y)` qu'il faut privilégier au lieu de `.pack()`.
4. **Dessin Artistique :** Apprenez via les objets `.create_line()` et `.create_oval()` de l'objet natif puissant `tk.Canvas`.
5. **Interactions :** Découvrez les événements via `.bind("<Enter>", callback)` pour créer des effets visuels au survol de la souris.

*En cliquant sur une leçon, le code d'exercice remplace votre propre code en cours.*

---

## 8. Astuces et Raccourcis Claviers

Dernières astuces pour maîtriser l'application :
- **Appuyez sur `F5`** n'importe quand depuis la zone Éditeur pour re-générer l'UI sans naviguer avec la souris.
- **Utilisez `Ctrl + S`** (Ou Cmd+S sur Mac) pour enregistrer rapidement votre code-source dans un fichier `.py` sur votre ordinateur.
- **Basculez ("Toggle")** l'inspecteur d'arborescence (icône de gauche en forme de Dossier) si vous avez besoin de plus de place pour l'éditeur !

### Bonne programmation sur TkLearn Studio ! 
