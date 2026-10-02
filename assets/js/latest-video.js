const LATEST_VIDEO_JSON = "./data/latest-video.json";

async function getLatestVideo() {
  try {
    const response = await fetch(LATEST_VIDEO_JSON, { cache: "no-cache" });

    if (!response.ok) {
      return null;
    }

    const video = await response.json();

    if (!video.videoId || !video.title || !video.url) {
      return null;
    }

    return video;
  } catch (error) {
    console.error("Error loading latest video:", error);
    return null;
  }
}

function createElement(tag, className, text) {
  const element = document.createElement(tag);

  if (className) {
    element.className = className;
  }

  if (text) {
    element.textContent = text;
  }

  return element;
}

async function renderLatestVideo() {
  const section = document.querySelector(".latest-video");
  const container = document.querySelector("#latest-video");

  if (!section || !container) {
    return;
  }

  const video = await getLatestVideo();

  if (!video) {
    section.hidden = true;
    return;
  }

  const link = createElement("a", "latest-video-link");
  link.href = video.url;
  link.target = "_blank";
  link.rel = "noopener noreferrer";

  const image = createElement("img");
  image.src = video.thumbnail;
  image.alt = video.title;
  image.loading = "lazy";

  const info = createElement("div", "latest-video-info");
  info.append(createElement("h3", null, video.title));

  if (video.published) {
    const date = new Date(video.published).toLocaleDateString("es-CL", {
      day: "numeric",
      month: "long",
      year: "numeric"
    });

    info.append(createElement("p", null, date));
  }

  info.append(createElement("span", null, "▶ Ver episodio"));

  link.append(image, info);
  container.replaceChildren(link);
}

renderLatestVideo();
