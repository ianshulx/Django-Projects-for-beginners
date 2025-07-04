console.log("📦 popup.js loaded");

document.getElementById("getHelp").addEventListener("click", async () => {
  const output = document.getElementById("output");
  const loader = document.getElementById("loader");

  //show loader
  loader.style.display = "block";
  output.innerHTML = "";

  try {
    chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
      const tab = tabs[0];
      const url = tab.url;
      const title = tab.title;

      console.log("LeetCode URL:", url);
      console.log("Problem Title:", title);

      const response = await fetch("https://leetcode-helper-wn4c.onrender.com/api/solve/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ title, url })
      });

      const data = await response.json();
      console.log("✅ Response from Django:", data);

      // hide loader
      loader.style.display = "none";

      if (data.steps && Array.isArray(data.steps)) {
        data.steps.forEach((step) => {
          const div = document.createElement("div");
          div.innerHTML = marked.parse(step); // Render markdown
          output.appendChild(div);

          document.getElementById("copyContainer").style.display = "block";

          // Copy text logic
          document.getElementById("copyBtn").onclick = () => {
            const textToCopy = data.steps.join('\n\n');
            navigator.clipboard.writeText(textToCopy).then(() => {
              document.getElementById("copyBtn").innerText = "✅";
              setTimeout(() => {
                document.getElementById("copyBtn").innerText = "Copy";
              }, 1500);
            })
          };

        });
      } else {
        output.innerHTML = "<p>No steps found.</p>";
      }
    });
  } catch (err) {
    loader.style.display = "none";
    output.innerHTML = "<p style='color: red;'>Error fetching data. Try again?</p>";
    console.error("❌ Error:", err);
  }
});
