$(document).ready(function () {
  console.log("ready!");

  function playWithoutToken() {
    // You'll need the playback URL from CDK output or retrieve it from IVS dashboard.
    var PLAYBACK_URL =
      "https://9dc154f9ed9c.us-east-1.playback.live-video.net/api/video/v1/us-east-1.194989662172.channel.SkwMfWDzfhfL.m3u8";
    registerIVSTech(videojs);

    var fn_metadata = function (event) {
      var payload = JSON.parse(event.text);
      console.log(event);
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
  }

  function playWithToken() {
    var jqxhr = $.get(
      "https://6yxngfe9s9.execute-api.us-east-1.amazonaws.com/prod/sign",
      function (data) {
        console.log(data);
        var token = data.token;
        var PLAYBACK_URL =
          "https://9dc154f9ed9c.us-east-1.playback.live-video.net/api/video/v1/us-east-1.194989662172.channel.SkwMfWDzfhfL.m3u8?token=" +
          token;
        registerIVSTech(videojs);

        var fn_metadata = function (event) {
          var payload = JSON.parse(event.text);
          console.log(event);
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
      }
    )
      .done(function () {})
      .fail(function () {})
      .always(function () {});
  }

  $("#btn-playWithoutToken").click(function () {
    console.log("Triggered playWithoutToken");
    playWithoutToken();
  });

  $("#btn-playWithToken").click(function () {
    console.log("Triggered playWithToken");
    playWithToken();
  });
});
