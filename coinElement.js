var paraCoin = document.registerElement("p-coin", {
	prototype: Object.create(HTMLParagraphElement.prototype),
	extends: "p"
});

Object.defineProperty(paraCoin, "coin-id", {
	value: "",
	writable: true
});

paraCoin.addEventListener("click", function(e){
	window.location = "https://www.google.com";
});