(function play() {
  // You'll need the playback URL from CDK output or retrieve it from IVS dashboard.
  var PLAYBACK_URL = "";
  registerIVSTech(videojs);

  var fn_metadata = function (event) {
    var payload = JSON.parse(event.text);
    var metadata_div = document.getElementById("metadata-container");
    var metadata_content_div = document.createElement("div");
    metadata_content_div.innerHTML =
      "<pre>" + JSON.stringify(payload) + "</pre>";
    metadata_div.appendChild(metadata_content_div);
  };

  var player = videojs(
    "amazon-ivs-videojs",
    {
      techOrder: ["AmazonIVS"],
    },
    () => {
      player.src(PLAYBACK_URL);
    }
  );
  const PlayerEventType = player.getIVSEvents().PlayerEventType;
  player
    .getIVSPlayer()
    .addEventListener(PlayerEventType.TEXT_METADATA_CUE, fn_metadata);
})();
