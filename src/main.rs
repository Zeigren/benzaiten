use serenity::http::Http;
use serenity::model::channel::Embed;
use std::sync::Arc;

fn main() {
    let id = 80088008;
    let token = "Discord Token";
    let http = Arc::new(Http::default());
    let webhook = http
        .as_ref()
        .get_webhook_with_token(id, token)
        .expect("valid webhook");

    let embed = Embed::fake(|e| {
        e.title("Title");
        e.description("Description");
        e.url("https://rust-lang.org");
        e.field("1st field", "Has some content.", true);
        e.field("2nd field", "Has some content.", true);
        e.field("3rd field", "Has some content.", true);
        e.colour(0xD917D3);
        e.thumbnail("https://www.iizcat.com/uploads/2016/10/njl87-jb11.jpg");
        e.timestamp("2004-06-08T16:04:23");
        e.author(|a| a.name("Author"));
        e.footer(|f| f.text("Footer"));

        e
    });

    let _ = webhook.execute(&http, false, |w| {
        w.embeds(vec![embed]);

        w
    });
}
