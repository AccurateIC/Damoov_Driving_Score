<div align="center">
  <a href="https://github-readme-tech-stack.vercel.app">
    <img src="https://github-readme-tech-stack.vercel.app/api/cards?title=Damoove+Tech+Stacks&align=center&titleAlign=center&fontSize=20&lineHeight=10&lineCount=2&theme=ayu&width=500&bg=%25230B0E14&titleColor=%231c9eff&line1=python%2Cpython%2Cauto%3Bflask%2Cflask%2Cauto%3Bnode.js%2Cnode.js%2Cauto%3B&line2=tailwindcss%2Ctailwind%2Cauto%3Breact%2Creact%2Cauto%3Bbruno%2Cbruno%2Cauto%3Bicons%2Cicons%2Cauto%3B" alt="Damoove Tech Stacks" />
  </a>
</div>

# 🚗 Damoov Driving Score

A project for analyzing and visualizing driving behavior, safety trends, and trip data.

---

## ⚙️ Software Requirements

- **Python 3.10+**
- **pip / virtualenv**
- **npm** (comes with Node.js)
- **Node.js v18+**
- **MySQL**

---

## 📥 Clone Repository

```bash
git clone https://github.com/AccurateIC/Damoov_Driving_Score.git
cd Damoov_Driving_Score
```

## ⚡ One-Step Setup
```bash
We provide a setup script to install everything at once.
This will install both frontend & backend environments automatically.

cd scripts

run this command if you are doing setup first time 
chmod +x install.sh

./install.sh
```

## 🖥️ Run in Development Mode

```bash
To start both backend and frontend in dev mode:

cd scripts

chmod +x dev.sh

./dev.sh

```

## 📂 Project Structure

```bash
Damoov_Driving_Score/
│── Backend/
│   ├── src/
│   │   ├── app/            # API & controllers
│   │   │   ├── controllers
│   │   │   ├── routes
│   │   │   ├── utils       # Utilities
│   │   └── flask_server.py # Main server file
│   └── requirements.txt
│
│── Frontend/               # React app
│   ├── src/                # Components & pages
│   ├── package.json
│   └── vite.config.js
│
│── scripts/                # Automation scripts
│   ├── install.sh
│   └── dev.sh
│
└── README.md
```


