

## Số liệu sự tương đồng câu giữa đoạn tóm tắt đơn và các nguồn dữ liệu (section, article)

**1.Phương pháp so sánh**

- Các đoạn được tách bằng spacy thành danh sách các câu
- Từ các đoạn của nguồn dữ liệu đối chiếu với đoạn tóm tắt đơn để tìm ra các câu xuất hiện theo thứ tự (của đoạn tóm tắt, và id của nó trong đoạn nguồn)

> Ví dụ:
> 
> Đoạn nguồn: A,M,F,R,J,G
> 
> Đoạn tóm tắt: A,F,G
> 
> Output = [ 0 2 5 ]
> 
> Dãy trên không có tính liên tiếp, nên so sánh này được gán nhãn FALSE
> 
> *( hiện tại, liên tiếp ở đây được định nghĩa là có tối thiểu 2 id liên tiếp nhau )*

**2. Các câu như thế nào được gọi là giống nhau (tức là coi 2 câu như 1, chứ không phải khoảng cách)?**

+ do dữ liệu article tồn tại nhiễu, nên công thức để coi 2 câu giống nhau:
	

> 	điểm = Trung bình cộng ( Số từ ngữ trong câu i mà có trong câu j /
> Tổng số từ câu i)

*trong đó:*
*- Mỗi từ chỉ được xét 1 lần*
*- Ngưỡng được chọn để coi 2 câu giống nhau là 0.8 (tức là tập từ vựng trung bình của 2 câu phải giống nhau ít nhất 80% thì được coi là 1 câu)*

**3. Kết quả**
a. nguồn đối chiếu section:
**![](https://lh4.googleusercontent.com/ZMBesiATYEknBHe0g5rThmVfhv02_PsCK0IUe2Bk83qHGO7D2pIaFWKJmXYGd8iYf45r8F3gdxNhCODaA25Efo8HN_4HmuJaXCww7JMcmMAzSafKcha3xEwyb9iEAvd4guw1O5QA)**

b. nguồn đối chiếu article:
**![](https://lh4.googleusercontent.com/ZMBesiATYEknBHe0g5rThmVfhv02_PsCK0IUe2Bk83qHGO7D2pIaFWKJmXYGd8iYf45r8F3gdxNhCODaA25Efo8HN_4HmuJaXCww7JMcmMAzSafKcha3xEwyb9iEAvd4guw1O5QA)**
**4. nhận xét, lưu ý**
- tách câu chỉ mang ý nghĩa tương đối (thao tác = spacy), chứ không hiểu theo bối cảnh ngữ nghĩa
- do vậy, trong article tồn tại nhiều câu không có ngắt nghỉ. các câu này tồn tại ở số ít tóm tắt
- dữ liệu section bớt nhiễu hơn article
- em có khảo sát qua thì thấy tồn tại một số câu mà trong tóm tắt không có từ vựng của (hoặc article hoặc section, các phần list trống []), do vậy hiện tại em đang nghi ngờ bản section không chỉ là bản cắt mà còn được chỉnh sửa mạnh hơn so với article, em sẽ hoàn thành khảo sát điều này trước buổi họp nhóm vào tối thứ 2

**5. kết luận**
- nhận định lấy theo các câu liên tiếp là có cơ sở và có thể áp dụng
