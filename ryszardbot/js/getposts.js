var rawPosts = document.querySelectorAll("[role=article][id*=post]");
var posts = [];

for (var i = 0; i < rawPosts.length; i++) {
	posts[i] = {}
	posts[i].likeCount = rawPosts[i].querySelector("[data-testid*=ReactionsCount]") || 0;
	if (posts[i].likeCount) posts[i].likeCount = parseInt(posts[i].likeCount.innerText);
	posts[i].time = parseInt(rawPosts[i].querySelector("[data-utime]").getAttribute("data-utime"));
	posts[i].text = rawPosts[i].querySelector("[data-testid=post_message]");
	if (posts[i].text) posts[i].text = posts[i].text.innerText;
	posts[i].author = rawPosts[i].querySelector("a[title]").title;
	posts[i].image = rawPosts[i].querySelector("img[data-src]");
	if (posts[i].image) posts[i].image = posts[i].image.src;
	posts[i].admin = rawPosts[i].querySelector("div[data-testid=story-subtitle] a[href*='badge_type=ADMIN']") != null;
	posts[i].permalink = rawPosts[i].querySelector("a[href*=permalink]").href;
}

return posts;
