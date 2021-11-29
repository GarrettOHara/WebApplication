function loadJsFile(filename, dataIsLoaded) {
  var fileref = document.createElement('script');
  fileref.setAttribute("type", "text/javascript");
  fileref.setAttribute("src", filename);
  fileref.onload = dataIsLoaded;

  if (typeof fileref != "undefined") {
    document.getElementsByTagName("head")[0].appendChild(fileref);
  }
}

/* The callback that is invoked when the file is loaded */
function dataIsLoaded() {
  console.log("Your data is ready to use");
}