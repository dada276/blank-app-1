<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>FruitSafe</title>
  <style>
    body {
      font-family: 'Segoe UI', sans-serif;
      background-color: #fffde9;
      text-align: center;
      padding: 30px;
      max-width: 600px;
      margin: auto;
    }

    .title {
      font-family: 'Georgia', serif;
      font-size: 48px;
      font-weight: bold;
      color: #2e8b57;
    }

    .icons {
      margin: 20px 0;
    }

    .icons img {
      width: 50px;
      margin: 0 20px;
      cursor: pointer;
    }

    video {
      width: 320px;
      height: 240px;
      background: black;
      border: 4px solid #2e8b57;
      border-radius: 10px;
    }

    .progress-bar {
      width: 60%;
      height: 15px;
      background-color: #ddd;
      margin: 10px auto;
      border-radius: 8px;
      overflow: hidden;
    }

    .progress-fill {
      height: 100%;
      width: 0%;
      background-color: #ffa500;
      transition: width 0.1s;
    }

    .results {
      font-size: 24px;
      color: #ff8c00;
      margin-top: 30px;
    }

    .clean-result {
      font-size: 36px;
      font-weight: bold;
      color: #228b22;
      transition: color 0.3s;
    }

    #suggestionText {
      font-size: 22px;
      font-style: italic;
      margin-top: 12px;
      color: #555;
      min-height: 28px;
    }

    #startBtn {
      margin-top: 20px;
      padding: 10px 20px;
      background-color: #2e8b57;
      color: white;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      font-size: 18px;
    }

    #startBtn:hover {
      background-color: #276744;
    }

    #historyView {
      display: none;
      text-align: left;
      color: #2e8b57;
    }

    #historyView h2 {
      font-family: 'Georgia', serif;
      text-align: center;
    }

    #historyList {
      list-style-type: decimal;
      padding-left: 20px;
      font-size: 20px;
      margin-top: 10px;
      max-height: 300px;
      overflow-y: auto;
    }

    #historyView button {
      margin-top: 20px;
      padding: 10px 20px;
      background-color: #2e8b57;
      color: white;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      font-size: 18px;
    }

    #historyView button:hover {
      background-color: #276744;
    }
  </style>
</head>
<body>

  <div class="title">Fruit<br>Safe</div>

  <div class="icons">
    <img id="scanIcon" src="https://img.icons8.com/ios-filled/50/scan-stock.png" alt="scan" title="Scan" />
    <img id="historyIcon" src="https://img.icons8.com/ios-filled/50/time.png" alt="time" title="View History" />
  </div>

  <!-- Scan View -->
  <div id="scanView">
    <video id="camera" autoplay playsinline></video>

    <div class="progress-bar">
      <div class="progress-fill" id="progressFill"></div>
    </div>
    <div id="scanText">waiting to scan...</div>

    <div class="results">results</div>
    <div class="clean-result" id="resultText">--</div>
    <div id="suggestionText"></div>

    <button id="startBtn">Start Scan</button>
  </div>

  <!-- History View -->
  <div id="historyView">
    <h2>Scan History</h2>
    <ul id="historyList"></ul>
    <button id="clearBtn">Clear History</button>
  </div>

  <script>
    const video = document.getElementById('camera');
    const progressFill = document.getElementById("progressFill");
    const scanText = document.getElementById("scanText");
    const resultText = document.getElementById("resultText");
    const suggestionText = document.getElementById("suggestionText");
    const startBtn = document.getElementById("startBtn");

    const historyIcon = document.getElementById("historyIcon");
    const scanIcon = document.getElementById("scanIcon");
    const scanView = document.getElementById("scanView");
    const historyView = document.getElementById("historyView");
    const historyList = document.getElementById("historyList");
    const clearBtn = document.getElementById("clearBtn");

    // Webcam access
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        video.srcObject = stream;
      })
      .catch(err => {
        alert("Could not access the camera. Please allow permission.");
        console.error(err);
      });

    let scanning = false;

    function getRandomPercentage() {
      return Math.floor(Math.random() * 101); // 0 to 100 inclusive
    }

    function updateResultColorAndSuggestion(percent) {
      if (percent >= 81) {
        resultText.style.color = '#228b22'; // green
        suggestionText.textContent = "Clean — safe to eat!";
      } else if (percent >= 60) {
        resultText.style.color = '#ff8c00'; // orange
        suggestionText.textContent = "Moderate — consider rinsing.";
      } else {
        resultText.style.color = '#cc0000'; // red
        suggestionText.textContent = "Needs Rewash — please wash thoroughly!";
      }
    }

    function formatDateTime(date) {
      const yyyy = date.getFullYear();
      const mm = String(date.getMonth() + 1).padStart(2, '0');
      const dd = String(date.getDate()).padStart(2, '0');
      const hh = String(date.getHours()).padStart(2, '0');
      const min = String(date.getMinutes()).padStart(2, '0');
      const ss = String(date.getSeconds()).padStart(2, '0');
      return `${yyyy}-${mm}-${dd} ${hh}:${min}:${ss}`;
    }

    function startScan() {
      if (scanning) return;
      scanning = true;
      progressFill.style.width = "0%";
      scanText.textContent = "scanning...0%";
      resultText.textContent = "--";
      suggestionText.textContent = "";
      resultText.style.color = '#228b22';

      let progress = 0;

      const interval = setInterval(() => {
        if (Math.random() < 0.15 && progress < 100) {
          scanText.textContent = "analyzing frame...";
          return;
        }

        progress += 2;
        if (progress > 100) progress = 100;
        progressFill.style.width = progress + "%";
        scanText.textContent = "scanning..." + progress + "%";

        if (progress >= 100) {
          clearInterval(interval);
          scanText.textContent = "scanning complete";

          const detected = Math.random() < 0.9;

          if (detected) {
            const cleanPercentage = getRandomPercentage();
            resultText.textContent = cleanPercentage + "% clean";
            updateResultColorAndSuggestion(cleanPercentage);

            let history = JSON.parse(localStorage.getItem('scanHistory') || "[]");
            const timestamp = formatDateTime(new Date());
            history.push({ time: timestamp, result: cleanPercentage + "% clean" });
            localStorage.setItem('scanHistory', JSON.stringify(history));
          } else {
            resultText.textContent = "No guava detected.";
            resultText.style.color = "#555555";
            suggestionText.textContent = "";
          }

          scanning = false;
        }
      }, 200);
    }

    function loadHistory() {
      let history = JSON.parse(localStorage.getItem('scanHistory') || "[]");
      historyList.innerHTML = "";

      if (history.length === 0) {
        historyList.innerHTML = "<li>No scan history available.</li>";
      } else {
        history.forEach((item) => {
          const li = document.createElement('li');
          li.textContent = `[${item.time}] - Result: ${item.result}`;
          historyList.appendChild(li);
        });
      }
    }

    clearBtn.addEventListener('click', () => {
      localStorage.removeItem('scanHistory');
      loadHistory();
    });

    historyIcon.addEventListener('click', () => {
      if (scanning) return;
      scanView.style.display = "none";
      historyView.style.display = "block";
      loadHistory();
    });

    scanIcon.addEventListener('click', () => {
      scanView.style.display = "block";
      historyView.style.display = "none";
    });

    startBtn.addEventListener('click', () => {
      startScan();
    });
  </script>

</body>
</html>


    startBtn.addEventListener('click', () => {
      startScan();
    });
  </script>

</body>
</html>
