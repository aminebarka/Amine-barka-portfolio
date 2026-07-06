import "./main.css";
import WebGL from "./webgl";

WebGL();

window.onerror = function(msg, url, line, col, error) {
  alert("Error: " + msg + "\nurl: " + url + "\nline: " + line);
};
const root = document.documentElement;

function onScroll() {
  if (window.scrollY > 10) root.dataset.scroll = "true";
  else root.dataset.scroll = "false";
}
onScroll();
window.addEventListener("scroll", onScroll, { passive: true });
