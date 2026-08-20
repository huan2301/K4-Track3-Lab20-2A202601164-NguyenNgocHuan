# Đánh giá chéo

## Chấm điểm theo rubric

| Tiêu chí | Điểm (0-2) | Bằng chứng |
|---|---:|---|
| Mức độ rõ ràng của vai trò | 2 | Supervisor định tuyến; Researcher tìm kiếm; Analyst đánh giá; Writer tổng hợp và trích dẫn. |
| Thiết kế state | 2 | `ResearchState` lưu sources, research notes, analysis notes, final answer, route history, trace và errors. |
| Guardrail khi lỗi | 1 | Có `max_iterations`, validation, fallback của provider và errors; chính sách timeout/retry chưa được áp dụng nhất quán cho mọi worker. |
| Benchmark | 2 | Baseline và multi-agent được so sánh theo latency, cost, quality proxy, citation coverage và failure rate. |
| Giải thích trace | 2 | Tên các node LangSmith đã được cấu hình; trace JSONL local trong `reports/traces/` là bằng chứng có thể kiểm tra. |
| **Tổng điểm** | **9/10** | Cài đặt tốt, còn thiếu một phần guardrail. |

## Feedback

**Strength:** Workflow có các bước bàn giao rõ ràng và bảo toàn source ID thông qua `research_notes`, `analysis_notes` và `final_answer`. Benchmark làm rõ sự đánh đổi giữa latency/cost/citation thay vì chỉ đánh giá kết quả dựa trên hình thức.

**Risk / failure mode:** Lỗi provider hoặc lỗi tìm kiếm có thể làm giảm chất lượng câu trả lời; fallback hiện tại có thể vẫn trông như chạy thành công nếu trạng thái degraded không được hiển thị rõ ràng. Test skeleton hiện tại vẫn yêu cầu `StudentTodoError`, mặc dù Supervisor đã được triển khai.

**One concrete improvement:** Thêm flag có kiểu `degraded` và áp dụng chính sách timeout/retry thống nhất cho mọi lời gọi provider và worker; thay test skeleton đã lỗi thời bằng một kiểm tra routing trước khi nộp bài.

**Score:** 9/10
