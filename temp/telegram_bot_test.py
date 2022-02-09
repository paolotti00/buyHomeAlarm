from bson import ObjectId

import functions_bot_telegram as bot_telegram
from classes import Home
from functions_repository import Repository

bot_telegram.start_bot()
# bot_telegram.send_text("test1","-651042114")
# bot_telegram.send_keyboard("-651042114")
repositoty = Repository()
home = repositoty.get_home_by_id_from_site("immobiliare_link_ad_93006632")[0]
# bot_telegram.send_as_html("-651042114", '<b>bold</b>, <strong>bold</strong> <i>italic</i>, <em>italic</em> <u>underline</u>, <ins>underline</ins> <s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del> <span class="tg-spoiler">spoiler</span>, <tg-spoiler>spoiler</tg-spoiler> <b>bold <i>italic bold <s>italic bold strikethrough <span class="tg-spoiler">italic bold strikethrough spoiler</span></s> <u>underline italic bold</u></i> bold</b> <a href="http://www.example.com/">inline URL</a> <a href="tg://user?id=123456789">inline mention of a user</a> <code>inline fixed-width code</code> <pre>pre-formatted fixed-width code block</pre> <pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>')

bot_telegram.send_as_html("-651042114",
                          ("<b>da: </b> {origin_site} \n" +
                           "<b>{title}</b> \n" +
                           "<b>Descrizione: breve </b> {description_short} \n" +
                           "<b>prezzo:</b> {price} \n" +
                           "<b>mt2:</b> {mt2} | <b>zona:</b> {zone} \n" +
                           "<b>piano:</b> {floor} | <b>locali:</b> {n_rooms} \n" +
                           "<b>bagni:</b> {n_bath_rooms} | <b>data annuncio:</b> {date} \n" +
                           "\n" +
                           " {description}" +
                           "\n" +
                           "\n" +
                           "<a href='{link_detail}'> vai a vederlo!</a>" +
                           "\n" +
                           "\n")
                          .format(origin_site=home.origin_site,
                                  title=home.title,
                                  description_short=home.description_short,
                                  price=home.price,
                                  mt2=home.mt2,
                                  zone=home.zone,
                                  floor=home.floor,
                                  n_rooms=home.n_rooms,
                                  n_bath_rooms=home.n_bath_rooms,
                                  date=home.date,
                                  description=home.description,
                                  link_detail=home.link_detail))
