//obtain list of posts elements
const rawPosts = document.querySelectorAll("[role=article][id*=post]");
const posts = [];

//create post models from raw data
for (let i = 0; i < rawPosts.length; i++) {
	posts[i] = {};
	
	//get like count, account for no likes and >1000 likes
	posts[i].likeCount = rawPosts[i].querySelector("[data-testid*=ReactionsCount] span[aria-hidden=true]") || 0;
	if (posts[i].likeCount) {
		if (posts[i].likeCount.innerText.indexOf("K") == -1)
			posts[i].likeCount = parseInt(posts[i].likeCount.innerText);
		else
			posts[i].likeCount = parseFloat(posts[i].likeCount.innerText) * 1000;
	}
	
	//extract author, time and permalink from always-existing elements
	posts[i].author = rawPosts[i].querySelector("a[title]").title;
	posts[i].time = parseInt(rawPosts[i].querySelector("[data-utime]").getAttribute("data-utime"));
	posts[i].permalink = rawPosts[i].querySelector("div[data-testid=story-subtitle] a[href*=permalink]").href;
	
	//extract text and image if respective elements exist
	posts[i].text = rawPosts[i].querySelector("[data-testid=post_message]");
	if (posts[i].text) posts[i].text = posts[i].text.innerText;
	posts[i].image = rawPosts[i].querySelector("img[data-src]");
	if (posts[i].image) posts[i].image = posts[i].image.src;
	
	//check for adminship or moderatorship by checking if badges exist
	posts[i].admin = rawPosts[i].querySelector("div[data-testid=story-subtitle] a[href*='badge_type=ADMIN']") != null;
	posts[i].moderator = rawPosts[i].querySelector("div[data-testid=story-subtitle] a[href*='badge_type=MODERATOR']") != null;
}

return posts;
