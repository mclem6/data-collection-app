(function () {
  const MAX_SECONDS = 60;
  const CANDIDATE_TYPES = [
    "audio/webm;codecs=opus",
    "audio/webm",
    "audio/mp4",
    "audio/ogg;codecs=opus",
  ];

  const audioInput = document.getElementById("id_audio");
  if (!audioInput) return;

  const canRecord = !!(
    navigator.mediaDevices &&
    navigator.mediaDevices.getUserMedia &&
    window.MediaRecorder
  );
  if (!canRecord) return; // leave the normal file upload in place

  const form = audioInput.closest("form");
  const wrapper = audioInput.closest("p") || audioInput.parentElement;

  // Build the recorder controls and hide the plain file input
  const ui = document.createElement("div");
  ui.innerHTML = `
    <p id="rec-status"></p>
    <button type="button" id="rec-start">Record</button>
    <button type="button" id="rec-stop">Stop</button>
    <button type="button" id="rec-redo">Re-record</button>
    <audio id="rec-playback" controls></audio>
  `;
  wrapper.insertAdjacentElement("beforebegin", ui);
  wrapper.hidden = true;
  audioInput.required = false; // a hidden required input would block submitting

  const status = ui.querySelector("#rec-status");
  const startBtn = ui.querySelector("#rec-start");
  const stopBtn = ui.querySelector("#rec-stop");
  const redoBtn = ui.querySelector("#rec-redo");
  const playback = ui.querySelector("#rec-playback");

  let recorder = null;
  let stream = null;
  let chunks = [];
  let timer = null;
  let seconds = 0;
  let objectUrl = null;

  function setState(state) {
    startBtn.hidden = state !== "idle";
    stopBtn.hidden = state !== "recording";
    redoBtn.hidden = state !== "recorded";
    playback.hidden = state !== "recorded";
  }

  function pickType() {
    return CANDIDATE_TYPES.find((t) => MediaRecorder.isTypeSupported(t)) || "";
  }

  function extensionFor(type) {
    if (type.includes("mp4")) return "m4a";
    if (type.includes("ogg")) return "ogg";
    return "webm";
  }

  function formatTime(s) {
    return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
  }

  function tick() {
    seconds += 1;
    status.textContent = `Recording... ${formatTime(seconds)}`;
    if (seconds >= MAX_SECONDS) stopRecording();
  }

  async function startRecording() {
    try {
      stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    } catch (err) {
      status.textContent =
        "Couldn't use the microphone. Check your browser's permission and try again.";
      return;
    }
    const mimeType = pickType();
    recorder = mimeType
      ? new MediaRecorder(stream, { mimeType })
      : new MediaRecorder(stream);
    chunks = [];
    recorder.addEventListener("dataavailable", (e) => {
      if (e.data.size > 0) chunks.push(e.data);
    });
    recorder.addEventListener("stop", finishRecording);
    recorder.start();
    seconds = 0;
    status.textContent = "Recording... 0:00";
    timer = setInterval(tick, 1000);
    setState("recording");
  }

  function stopRecording() {
    clearInterval(timer);
    if (recorder && recorder.state === "recording") recorder.stop();
  }

  function finishRecording() {
    stream.getTracks().forEach((t) => t.stop()); // turns the mic indicator off

    const type = (recorder.mimeType || "audio/webm").split(";")[0];
    const blob = new Blob(chunks, { type });
    if (blob.size === 0) {
      status.textContent = "Nothing was recorded. Please try again.";
      setState("idle");
      return;
    }

    const file = new File([blob], `recording.${extensionFor(type)}`, { type });
    const transfer = new DataTransfer();
    transfer.items.add(file);
    audioInput.files = transfer.files;

    if (objectUrl) URL.revokeObjectURL(objectUrl);
    objectUrl = URL.createObjectURL(blob);
    playback.src = objectUrl;

    status.textContent = "Listen back. Happy with it? Type what you said and submit.";
    setState("recorded");
  }

  function redo() {
    audioInput.value = "";
    playback.removeAttribute("src");
    status.textContent = "Press Record and say the sentence.";
    setState("idle");
  }

  startBtn.addEventListener("click", startRecording);
  stopBtn.addEventListener("click", stopRecording);
  redoBtn.addEventListener("click", redo);

  form.addEventListener("submit", (e) => {
    if (recorder && recorder.state === "recording") {
      e.preventDefault();
      status.textContent = "Press Stop before submitting.";
    } else if (!audioInput.files.length) {
      e.preventDefault();
      status.textContent = "Please record your voice before submitting.";
    }
  });

  status.textContent = "Press Record and say the sentence.";
  setState("idle");
})();