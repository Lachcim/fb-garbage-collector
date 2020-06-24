//get post container from permalink
const permalink = arguments[0].match(/permalink\/(\d+)\//)[1];
const postLink = document.querySelector("[role=article] a[href*=\"" + permalink + "\"]");
let post = postLink;
while (post.getAttribute("role") != "article")
	post = post.parentElement;

//helper function - resolves when query returns result
function waitForElement(query, inverted) {
	inverted = inverted || false;
	
	return new Promise(function (resolve, reject) {
		const start = new Date();
		let interval;
		
		function work() {
			if (new Date() - start >= 10000) {
				clearInterval(interval);
				reject();
			}
			
			const result = document.querySelector(query);
			if (Boolean(result) != inverted) {
				clearInterval(interval);
				resolve(result);
			}
		}
		
		interval = setInterval(work, 100);
	});
}

//click chevron and await post menu
post.querySelector("[data-testid=post_chevron_button]").click();
await waitForElement("div.uiContextualLayerPositioner:not(.hidden_elem) #post_menu");

//click delete option, unless there's none
const deleteOption = document.querySelector("a[data-feed-option-name=MallPostDeleteOption][ajaxify*='" + permalink + "']");
if (!deleteOption) return false;
deleteOption.click();

//wait for deletion dialog to appear and fill out form
await waitForElement("textarea[name=admin_notes]");
document.querySelector("textarea[name=admin_notes]").value = arguments[1];
document.querySelector("button.layerConfirm").click();

//wait for confirmation box
await waitForElement("[id='" + permalink + "'].uiBoxGray");
return true;
