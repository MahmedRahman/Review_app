async function fetchReviews() {
  console.log("hi");
  const appUrlInput = document.getElementById("app-url");
  const appUrl = appUrlInput.value;

  const spinner = document.getElementById("spinner");
  const reviewList = document.getElementById("review-list");

  const appId = extractAppId(appUrl);
  if (!appId) {
    alert("Invalid URL. Please enter a valid Google Play URL.");
    return;
  }

  reviewList.innerHTML = "";
  spinner.classList.remove("d-none");

  const response = await fetch(`/scrape_reply?app_id=${appId}`);
  const data = await response.json();

  spinner.classList.add("d-none");
  let row_box;
  for (const review of data.data.reviews) {
    
     row_box = `
    <div class="card mb-3">
    <div class="card-body">
    <h5 class="card-title">   ${review.at}</h5>
      <h5 class="card-title"> ${review.content}</h5>
      <p class="card-text"></p>
      <p id="replyElement">

      </p>
      <p class="card-text text-muted"></p>
      <button class="btn btn-primary d-flex align-items-center" onclick="${generateFriendlyReplyJS(event, review.content)}">
      Generate Friendly Reply
        <div class="spinner-border spinner-border-sm ms-2 d-none" role="status"><span class="visually-hidden">Loading...</span></div>
      </button>
    </div>
  </div>`;


 reviewList.innerHTML += row_box;
    
  }


}


async function generateFriendlyReplyJS(e,reviewText) {
  console.log(e.target)
  buttonSpinner.classList.remove("d-none");
  const replyElement = document.getElementById("replyElement"); 
  try {
    const response = await axios.post('/friendly_reply', {
      review_text: reviewText,
    });

    if (response.data) {
      console.log(response.data);
      replyElement.textContent = response.data["data"];
    } else {
      replyElement.textContent = 'Error generating friendly reply.';
      console.error('Error:', response.data.error, 'Details:', response.data.details);
    }
  } catch (error) {
    replyElement.textContent = 'Error generating friendly reply.';
    console.error('Error:', error);
  } finally {
    // Hide the spinner
    //buttonSpinner.classList.add("d-none");
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

document.addEventListener("DOMContentLoaded", function () {
  loadPartial("header", "/static/partials/header.html");
  loadPartial("footer", "/static/partials/footer.html");
});

async function loadPartial(elementId, partialUrl) {
  const element = document.getElementById(elementId);

  if (element) {
    try {
      const response = await fetch(partialUrl);

      if (response.status === 200) {
        const html = await response.text();
        element.innerHTML = html;
      } else {
        console.error(`Error ${response.status} while loading partial ${partialUrl}`);
      }
    } catch (error) {
      console.error(`Error while loading partial ${partialUrl}:`, error);
    }
  }
}

// The rest of the existing code

document.getElementById("fetch-reviews-button").addEventListener("click", fetchReviews);
