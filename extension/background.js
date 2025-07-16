chrome.action.onClicked.addListener((tab) => {
    console.log("LeetCode Visualizer icon clicked on tab:", tab.url);

    if (!tab.url.startsWith("https://leetcode.com/problems/")) {
        chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: () => {
                alert("⚠️ Please navigate to a LeetCode problem page before using the extension.");
            }
        });
    } else {
        chrome.scripting.executeScript({
            target: { tabId: tab.id },
            files: ["popup.js"]
        });
    }
});
