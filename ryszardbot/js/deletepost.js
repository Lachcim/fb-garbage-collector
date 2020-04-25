var permalink = arguments[0].substr(48);
var postLink = document.querySelector("a[href*=\"" + permalink + "\"]");
var post = postLink;
while (post.getAttribute("role") != "article")
	post = post.parentElement;

console.log("deleting post");

function waitForElement(query, inverted) {
	inverted = inverted || false;
	
	return new Promise(function (resolve, reject) {
		var start = new Date();
		var interval;
		
		function work() {
			if (new Date() - start >= 10000) {
				clearInterval(interval);
				reject();
			}
			
			var result = document.querySelector(query);
			if (Boolean(result) != inverted) {
				clearInterval(interval);
				resolve(result);
			}
		}
		
		interval = setInterval(work, 100);
	});
}
function wait(timeout) {
	return new Promise(function (resolve) {
		setTimeout(resolve, timeout);
	});
}

debugger;
console.log("clicking chevron");
post.querySelector("[data-testid=post_chevron_button]").click();
console.log("awaiting menu");
await waitForElement("div.uiContextualLayerPositioner:not(.hidden_elem) #post_menu");

console.log("seeking and clicking delete option");
var deleteOption = document.querySelector("a[data-feed-option-name=MallPostDeleteOption][ajaxify*='" + permalink.substr(10, 15) + "']");
if (!deleteOption) return false;
deleteOption.click();

console.log("awaiting deletion dialog")
await waitForElement("textarea[name=admin_notes]");
console.log("filling deletion form")
document.querySelector("textarea[name=admin_notes]").value = arguments[1];
document.querySelector("input[name=share_feedback]").checked = true;
document.querySelector("button.layerConfirm").click();

console.log("awaiting finalization");
await waitForElement("[id='" + permalink.substr(10, 15) + "'].uiBoxGray");
console.log("post deleted")
return true;
