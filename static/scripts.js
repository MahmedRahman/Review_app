async function fetchReviews() {
  const appUrlInput = document.getElementById("app-url");
  const appUrl = appUrlInput.value;
  const appId = extractAppId(appUrl);

  const spinner = document.getElementById("spinner");
  const reviewList = document.getElementById("review-list");

  if (!appId) {
    alert("Invalid URL. Please enter a valid Google Play URL.");
    return;
  }
  reviewList.innerHTML = "";
  spinner.classList.remove("d-none");

  const response = await fetch(`/scrape?app_id=${appId}`);
  const data = await response.json();

  spinner.classList.add("d-none");

  for (const review of data.reviews) {
    const card = document.createElement("div");
    card.className = "card mb-3";

    const cardBody = document.createElement("div");
    cardBody.className = "card-body";

    const cardTitle = document.createElement("h5");
    cardTitle.className = "card-title";
    cardTitle.textContent = `${review.author} (${review.date})`;

    const cardText = document.createElement("p");
    cardText.className = "card-text";
    cardText.textContent = review.review_text;

    const replyElement = document.createElement("p");
    replyElement.className = "card-text text-muted";
    replyElement.textContent = "";

    const cardButton = document.createElement("button");
    cardButton.className = "btn btn-primary d-flex align-items-center";
    cardButton.textContent = "Generate Friendly Reply";

    const buttonSpinner = document.createElement("div");
    buttonSpinner.className = "spinner-border spinner-border-sm ms-2 d-none";
    buttonSpinner.setAttribute("role", "status");
    buttonSpinner.innerHTML = '<span class="visually-hidden">Loading...</span>';
    cardButton.appendChild(buttonSpinner);

    cardButton.onclick = function () {
      generateFriendlyReply(review.review_text, replyElement, buttonSpinner);
    };

    cardBody.appendChild(cardTitle);
    cardBody.appendChild(cardText);
    cardBody.appendChild(replyElement);
    cardBody.appendChild(cardButton);
    card.appendChild(cardBody);
    reviewList.appendChild(card);
  }
}

async function generateFriendlyReply(reviewText, replyElement, buttonSpinner) {
  buttonSpinner.classList.remove("d-none");

  const prompt = `Create a friendly reply to the following review:\n\n"${reviewText}"\n\nReply: `;
  const apiKey = "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";
  const apiUrl = "https://api.openai.com/v1/completions";

  try {
    const response = await axios.post(
      apiUrl,
      {
        model: "text-davinci-003",
        prompt: prompt,
        max_tokens: 50,
        temperature: 1,
        n: 1,
      },
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${apiKey}`,
        },
      }
    );

    const reply = response.data.choices[0].text.trim();
    replyElement.textContent = `Friendly reply: ${reply}`;
  } catch (error) {
    console.error("Error generating friendly reply:", error);

    handleApiError(error);
  } finally {
    // Hide the spinner
    buttonSpinner.classList.add("d-none");
  }
}

function extractAppId(url) {
  const match = url.match(/id=([\w\d_.]+)/);
  return match ? match[1] : null;
}

function handleApiError(error) {
  if (error.response) {
    switch (error.response.status) {
      case 400:
        alert("Error: Bad request. Please check your input and try again.");
        break;
      case 401:
        alert("Error: Unauthorized. Please check your API key and try again.");
        break;
      case 403:
        alert("Error: Forbidden. You do not have the required permissions to access the API. Please check your API key and try again.");
        break;
      case 404:
        alert("Error: Not found. The requested resource was not found on the server. Please check your input and try again.");
        break;
      case 429:
        alert("Error: You've reached the rate limit for the API. Please try again later.");
        break;
      case 500:
        alert("Error: Internal server error. The server encountered an error while processing your request. Please try again later.");
        break;
      default:
        alert("Error generating friendly reply. Please check console for details.");
    }
  } else {
    alert("Error generating friendly reply. Please check console for details.");
  }
}

document.getElementById("fetch-reviews-button").addEventListener("click", fetchReviews);
