window.onload = () => {
  let websocket = new WebSocket("ws://127.0.0.1:9999/");
  let updateTime = 5000;

  // Count how many elements on the page
  const countElements = () => {
    let tasks = $(".tasks")[0].id.split("_")[1];
    let reports = $(".reports")[0].id.split("_")[1];
    let checkThis = `${tasks},${reports}`;
    return checkThis;
  };

  const updatePage = () => {
    if (websocket.readyState == 1) {
      websocket.send(
        JSON.stringify({ action: "check", count: countElements() })
      );
    } else {
      console.warn("Connection lost, websocket is  unavailable");
    }
  };

  // Wait and comparing data
  websocket.onmessage = event => {
    let data = JSON.parse(event.data);
    switch (data.type) {
      case "state":
        if (countElements() != data.value) {
          $(".document").load("ajax .document");
        }
        break;
      default:
        console.error("unsupported event", data);
    }
  };

  websocket.onclose = event => {
    console.warn("Connection lost");
    console.warn("Invoke Javascript reload page");
  };

  // Updating page every 5 seconds by default
  window.setInterval(updatePage, updateTime);
};
