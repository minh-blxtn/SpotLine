================================================================================
                    SPOTLINE V2 (DUAL-MONITOR EDITION)
                CÔNG CỤ ĐO KHOẢNG CÁCH BẢN ĐỒ PUBG PC
================================================================================

1. GIỚI THIỆU
Spotline v2 là công cụ hỗ trợ đo khoảng cách chuẩn xác trên bản đồ PUBG (giúp zeroing súng ngắm hoặc chỉnh cự ly súng cối). 
Điểm khác biệt của V2: Loại bỏ hoàn toàn lớp màng trong suốt (Overlay) đè lên màn hình game. Thay vào đó, toàn bộ giao diện và kết quả đo đạc được chuyển sang hiển thị trên một Bảng điều khiển (Dashboard) đặt tại Màn hình phụ, giúp đảm bảo an toàn tuyệt đối và không gây tụt FPS.

--------------------------------------------------------------------------------
2. CƠ CHẾ AN TOÀN TUYỆT ĐỐI (100% Bypassed)
Phiên bản V2 đã khắc phục hoàn toàn rủi ro của V1 để đạt mức tàng hình tối đa trước hệ thống BattlEye / Zakynthos nhờ các nguyên lý:
- KHÔNG OVERLAY (Zero DXGI Hooking): App không còn vẽ đè lên màn hình chính. Anti-cheat không thể quét được bất kỳ sự can thiệp đồ họa nào vào vùng không gian của game.
- HỖ TRỢ FULLSCREEN EXCLUSIVE: Việc chuyển UI sang màn phụ cho phép bạn chơi PUBG ở chế độ Toàn màn hình thực sự (Fullscreen). Vừa triệt tiêu độ trễ (Input Lag), vừa chứng minh với Anti-cheat rằng bạn không dùng phần mềm thứ ba trên màn chính.
- ĐỌC TÍN HIỆU BỊ ĐỘNG (Passive Read-only): App chỉ "đọc" tọa độ chuột cục bộ trên hệ điều hành, tuyệt đối không gửi tín hiệu chuột giả mạo (SendInput) can thiệp vào game.
- HOẠT ĐỘNG OFFLINE: Không có hàm API nào quét bộ nhớ game hay phần cứng. Mọi thông số hoạt động đều do người dùng tự nhập thủ công tĩnh.

--------------------------------------------------------------------------------
3. HƯỚNG DẪN CHUẨN BỊ (Chỉ làm 1 lần)
- Yêu cầu phần cứng: Bắt buộc sử dụng hệ thống 2 màn hình (Dual Monitor).
- Cài đặt Game: Đặt PUBG ở chế độ Fullscreen (Toàn màn hình) trên màn hình chính để tối ưu FPS.
- Khởi động: Click chuột Right vào file tool -> Chọn "Run as Administrator".

--------------------------------------------------------------------------------
4. BẢNG CẤU HÌNH & Ý NGHĨA CÁC THÔNG SỐ 
Ở lần mở đầu tiên, hộp Cài đặt sẽ hiện lên ở giữa màn hình. Bạn cần nhập đúng để app hiểu không gian màn hình của bạn và không bị đo sai.

[1] Windows Scale (%): Tỷ lệ phóng to của Windows (trong mục Display Settings).
-> Công dụng: Khử sai số do Windows phóng to hình ảnh. Giúp app biết tỷ lệ thực tế để không bị đo ảo (100m thành 125m). Mặc định thường là 100.

[2] Màn chính (Windows X, Y): Độ phân giải thực tế ngoài Desktop của màn hình bạn dùng chơi game (VD: 1920 1080).
-> Công dụng: Xác định "kích thước vật lý" giới hạn của màn hình chính.

[3] Trong Game (X, Y): Độ phân giải Setting ở trong game PUBG (VD: 1440 1080).
-> Công dụng: Khử sai số méo hình. Nếu bạn chơi hình ảnh bị kéo giãn (Stretched) bè ra hai bên, app sẽ tự động bóp tỷ lệ lại để tính đường chéo chuẩn xác 100%. Nếu màn Desktop và Game giống hệt nhau, cứ nhập số giống nhau.

[4] Màn phụ (X, Y): Độ phân giải của màn hình thứ 2 (VD: 1920 1200).
-> Công dụng: Vì app hoạt động ẩn nên không biết màn hình phụ của bạn to nhỏ ra sao. Bạn nhập số này để app làm toán chia đôi, từ đó thả khung giao diện vào đúng CHÍNH GIỮA màn hình phụ cho dễ nhìn.

[5] Vị trí màn phụ (Left / Right): Màn hình phụ đang nằm ở bên nào so với màn chơi game.
-> Công dụng: Chỉ đường cho hệ thống tọa độ. Nếu chọn sai, app vẫn tính toán căn giữa nhưng sẽ ném khung thông báo về hướng không có cái màn hình nào cả, dẫn tới việc bạn không thấy bảng UI đâu.

>> TÍNH NĂNG AUTO-LOAD: 
Từ lần mở thứ 2 trở đi, app sẽ tự động đọc file "spotline_config.json" lưu từ trước và tự động ném hộp Cài đặt sang màn hình phụ. Bạn chỉ cần ấn phím [ENTER] là app bắt đầu chạy ngầm ngay lập tức.
Nếu gặp lỗi hộp UI không xuất hiện trên cả 2 màn sau khi chạy ( Đã bị mở nhầm ở vùng không gian ảo do vị trí màn phụ bị sai vì app đọc nhầm ) thì chỉ cần đóng app, xóa file spotline_config.json để app tự động đưa vị trí mặc định về chính giữa màn hình chính, sau đó chỉ cần chọn đúng vị trí màn phụ là sẽ hoạt động bình thường.
--------------------------------------------------------------------------------
5. PHÍM TẮT & THAO TÁC TRONG GAME
- Phím [ : Bật / Tắt (ON/OFF) chế độ đo lường.
- Phím ] : Đóng (Kill) phần mềm hoàn toàn.
* Lưu ý: Mọi thao tác click chuột lỡ tay rơi vào màn hình phụ sẽ tự động bị app từ chối (bỏ qua) để tránh lỗi.

--------------------------------------------------------------------------------
6. CÁCH ĐO KHOẢNG CÁCH (Kết quả báo ở màn hình phụ)

Bước 1: Cài đặt mốc 100m (Calibrating)
* Chỉ làm 1 lần lúc bắt đầu trận hoặc khi bạn thay đổi mức độ Zoom của bản đồ.
- Mở bản đồ (Phím M). Zoom bản đồ tới mức vừa đủ nhìn thấy bạn và mục tiêu.
- Giữ phím [CTRL] trên bàn phím.
- Dùng [Click Chuột Giữa] (Nút cuộn chuột) chấm vào 2 điểm đầu và cuối của 1 ô vuông 100m trên bản đồ.
- Nhìn sang màn hình phụ, app hiện chữ xanh "100m Set! Ratio: ..." -> Cài mốc thành công.

Bước 2: Đo khoảng cách thực tế (Measuring)
* Lưu ý: KHÔNG thay đổi mức Zoom bản đồ sau khi đã làm Bước 1.
- Thả phím [CTRL] ra.
- Dùng [Click Chuột Giữa] bấm vào vị trí bạn đang đứng.
- Tiếp tục [Click Chuột Giữa] bấm vào mục tiêu.
- Nhìn sang màn hình phụ, kết quả sẽ hiện thị tức thì: "RESULT: [Số mét] meters".
================================================================================