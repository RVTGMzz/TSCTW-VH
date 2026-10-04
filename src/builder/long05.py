import json
from pathlib import Path
R=Path(__file__).parent
rows=json.loads((R/'english.json').read_text())
extra=dict(l.split('\t',1) for l in (R/'extra05.tsv').read_text().splitlines() if l)
# Each tooltip's control fields following its description are preserved byte-for-byte.
human={
'Hunger':('Đói','Tìm thức ăn trong rương hành lý hoặc hái quả ăn được trên cây. Kỹ năng nấu ăn giúp Sim làm những bữa ngon hơn bên lửa trại. Nhấn H để Sim tự tìm đồ ăn.'),
'Energy':('Năng lượng','Một chỗ trú đơn sơ cũng giúp Sim mệt mỏi có nơi ngả lưng. Ăn hạt cà phê ngay trên bụi cây cũng tăng năng lượng. Nhấn R để Sim tìm chỗ ngủ.'),
'Comfort':('Thoải mái','Trên đảo vẫn có những chỗ nghỉ dễ chịu: một số tảng đá ngồi khá êm, và mái trú cũng là nơi đáng tin cậy. Nhấn M để Sim tìm chỗ thư giãn.'),
'Fun':('Giải trí','Vẻ đẹp tự nhiên của đảo Felicity có thể mang lại nhiều niềm vui. Sim có thể ngắm trời cả ngày lẫn đêm để thư giãn. Nhấn F để tìm hoạt động giải trí.'),
'Hygiene':('Vệ sinh','Nước máy không sẵn có, nhưng bơi dưới biển sẽ giúp Sim sạch hơn. Nhấn Y để Sim tự làm vệ sinh.'),
'Social':('Giao tiếp','Sim thích giao tiếp, dù trên đảo chẳng có mấy người. Viết nhật ký, viết thư về nhà hoặc trò chuyện với những thứ quanh mình có thể giúp vơi cô đơn. Nhấn L để đáp ứng nhu cầu giao tiếp.'),
'Bladder':('Tiểu tiện','Khi Sim cần đi vệ sinh, hãy đưa họ đến một bụi cây phù hợp hoặc nhà vệ sinh càng sớm càng tốt. Nhấn B để Sim tự giải quyết nhu cầu này.'),
'Environment':('Môi trường','Đồ trang trí và cảnh quan ảnh hưởng đến cảm nhận của Sim về nơi ở. Họ thích không gian sạch, sáng và nhiều màu sắc. Nhấn K để Sim dọn dẹp.'),
'Family':('Gia đình','Sự gắn bó với gia đình giúp Sim hạnh phúc. Ôm và trò chuyện với người thân sẽ đáp ứng nhu cầu này, đồng thời củng cố quan hệ.')}
skills={
'Cooking Skill':('Nấu ăn','Đọc sách và nấu nướng giúp Sim làm những bữa ăn ngon, no lâu hơn. Kỹ năng này đặc biệt hữu ích để tận dụng nguồn thức ăn trên đảo.'),
'Mechanical Skill':('Sửa chữa','Biết sửa đồ giúp cuộc sống trong trại thuận lợi hơn. Sim có thể học qua sách trong tủ hoặc rương hành lý, cũng như sửa những vật dụng bị hỏng.'),
'Charisma Skill':('Giao tiếp','Khả năng trò chuyện và sự tự tin giúp Sim kết bạn, giữ tình bạn. Luyện tập trước gương để nâng kỹ năng này. Sim thân thiện, hướng ngoại thường học tốt hơn.'),
'Body Skill':('Thể lực','Bơi ngoài biển giúp rèn sức mạnh, sự nhanh nhẹn và tốc độ. Thể lực rất hữu ích cho nghề Thợ săn. Sim năng động sẽ tiến bộ nhanh hơn.'),
'Logic Skill':('Tư duy','Rèn khả năng suy luận và tổ chức bằng sách hoặc kính thiên văn. Kỹ năng này hữu ích cho nghề Thợ chế tác và phù hợp cả với những Sim ít vận động.'),
'Creativity Skill':('Sáng tạo','Viết nhật ký giúp Sim phát triển khả năng sáng tạo. Kỹ năng này gồm nghệ thuật, âm nhạc và sáng chế, hữu ích cho nhiều nghề. Sim vui vẻ thường dễ phát huy hơn.'),
'Cleaning Skill':('Dọn dẹp','Một khu trại sạch sẽ giúp mọi người dễ chịu. Dọn nơi ở thường xuyên sẽ nâng kỹ năng, giúp công việc nhanh và nhẹ hơn. Sim ngăn nắp có lợi thế khi học kỹ năng này.')}
for x in rows:
 en=x['text'];parts=en.split('|')
 if x['file']=='Live.package' and x['id']==130 and len(parts)>=5 and parts[0] in human and ('0xab20' in en):
  title,body=human[parts[0]];extra[en]='|'.join([title,body]+parts[2:])
 if x['file']=='Live.package' and x['id']==137 and len(parts)>=5 and parts[0] in skills and 'Orangutan' not in en:
  title,body=skills[parts[0]];extra[en]='|'.join([title,body+'\n']+parts[2:])
extra.update({
"Satisfy your Sim's basic needs to keep their Mood in the green. Mood affects every aspect of a Sim's life, from how they interact with other Sims, to their Job Performance.":'Đáp ứng các nhu cầu cơ bản để giữ tâm trạng Sim ở mức xanh. Tâm trạng ảnh hưởng đến mọi mặt cuộc sống, từ giao tiếp đến hiệu quả làm việc.',
"Keyboard shortcuts can be used to help keep your Sim's Mood in the green.  Mouse over each need to find out what the specific shortcut is.":'Dùng phím tắt để chăm sóc nhu cầu của Sim. Rê chuột lên từng nhu cầu để xem phím tương ứng.',
"If you've never played The Sims before, this is a great place to get to know the game. Part One will teach you how to give commands to a friendly chap named Tutorial Joe and walk you through taking care of his basic needs.":'Nếu chưa từng chơi The Sims, đây là nơi thích hợp để bắt đầu. Phần một hướng dẫn bạn điều khiển anh chàng Tutorial Joe và chăm sóc các nhu cầu cơ bản của anh ấy.',
'Part Two of The Basics takes you into a small family of Sims to learn about social interactions and relationships.':'Phần hai đưa bạn đến một gia đình Sim nhỏ để làm quen với giao tiếp và các mối quan hệ.',
'Building a Home covers the very basics of residential construction. Learn about placing walls, doors, and windows, as well as handy shortcuts to things like painting walls and carpeting floors.':'Bài Xây tổ ấm giới thiệu cách dựng nhà cơ bản: đặt tường, cửa ra vào, cửa sổ, cùng các phím tắt tiện dụng để sơn tường và lát sàn.',
"New players and returning players alike will enjoy a tour of some of the new game play and controls in The Sims Castaway Stories. Learn about Sims' aspirations and familiarize yourself with their Wants.":'Khám phá cách chơi và điều khiển mới trong The Sims Castaway Stories. Bài hướng dẫn giới thiệu khát vọng của Sim và giúp bạn làm quen với những mong muốn của họ.',
'The Sims Castaway Stories adds even more features to building a home, including raised foundations and decks. New Building Tools will introduce you to the latest and greatest trends for Sim architects.':'The Sims Castaway Stories bổ sung nhiều cách xây nhà, gồm nền nâng cao và sàn hiên. Bài Công cụ xây dựng mới sẽ giới thiệu những tính năng này.',
"A toddler's job is growing up, and they have fun learning new skills. Supportive family members help them learn everything they need to know.":'Trẻ tập đi lớn lên qua việc vui chơi và học kỹ năng mới. Sự quan tâm của gia đình giúp trẻ học những điều cần thiết.',
"A child's job is becoming a teen, and they have fun learning new skills. Supportive family members help them learn everything they need to know.":'Trẻ em đang trên đường trở thành thiếu niên và thích học kỹ năng mới. Sự quan tâm của gia đình giúp các em trưởng thành.',
"Sailing the world on the crew of a luxury yacht has been rewarding, but lonely. Could that be about to change? The captain just announced that the ship is heading for shore leave at Meet Your Mate -- the hottest singles resort in the world! This is a once in a lifetime opportunity to meet the love of your life.":'Làm việc trên du thuyền sang trọng, đi khắp thế giới thật thú vị, nhưng cũng cô đơn. Liệu điều đó sắp thay đổi? Thuyền trưởng vừa thông báo cả đoàn sẽ lên bờ nghỉ tại Meet Your Mate, khu nghỉ dưỡng dành cho người độc thân nổi tiếng nhất thế giới! Đây có thể là cơ hội có một không hai để gặp tình yêu của đời mình.',
"Yesterday you were trapped in the daily grind back in Sim City. Today you're on your way to the hottest singles resort in the world to do a story for 'Going Places' magazine. It's a once in a lifetime opportunity, and not just for your writing career. Somewhere out there you're determined to find your own special someone.":'Mới hôm qua, bạn còn mắc kẹt trong nhịp sống lặp lại ở Sim City. Hôm nay, bạn đang đến khu nghỉ dưỡng dành cho người độc thân nổi tiếng nhất thế giới để viết bài cho tạp chí Going Places. Cơ hội hiếm có này còn mang ý nghĩa hơn cả sự nghiệp: đâu đó ngoài kia, bạn tin mình sẽ tìm được người đặc biệt.',
})
for n in range(1,25):extra['Chapter '+str(n)]='Chương '+str(n)
# Translate island introductions, preserving the information about unlock requirements.
for x in rows:
 if x['file']=='UIText.package' and x['id']==750:
  extra[x['text']]='Nhìn từ trên cao, Wanmami chẳng khác mấy những hòn đảo có người ở khác. Nhưng với những người sống sót sau tai nạn máy bay và đắm tàu, nơi này là đất liền quý giá sau chuỗi sự cố. Mặt trời luôn rực rỡ trên đảo Wanmami, trừ khi đã lặn, còn thời tiết thì đúng như một thiên đường nhiệt đới.\n\nLưu ý: Một số vật dụng cần thiết như rìu nhỏ, dao phát, điện thoại vỏ sò và máy phát điện gió chỉ được mở khóa sau khi hoàn thành Shipwrecked and Single. Bạn có thể tìm chúng trong mục Phần thưởng cốt truyện.'
 if x['file']=='UIText.package' and x['id']==755:
  extra[x['text']]='Ít ai biết về thiên đường nhiệt đới xa xôi này. Hòn đảo không được đánh dấu trên bất kỳ hải đồ hay bản đồ nào. Thú hoang lẩn khuất trong rừng rậm, từ miệng núi lửa đáng ngại đến những bãi cát mênh mông. Lạc lối và cô độc, liệu bạn có sống sót đủ lâu để tìm những người cùng cảnh ngộ và gặp cư dân bản địa?'
(R/'extra05.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2))
print('Extra translation mappings:',len(extra))
