# Frontend Architecture & Structure

This document describes the structure and technologies used in the frontend of the ChatBot project.

## 🛠 Technologies

- **Framework:** [Next.js](https://nextjs.org/) (App Router paradigm)
- **Language:** TypeScript
- **Styling:** Tailwind CSS (v3) + PostCSS
- **Package Manager:** npm

## 📁 Directory Structure

The `frontend` directory follows a standard and modern Next.js App Router structure:

```text
frontend/
├── app/                  # Next.js App Router: Routing, layouts, and pages
│   ├── globals.css       # Global CSS styles & Tailwind directives
│   ├── layout.tsx        # Root layout (HTML skeleton, global metadata)
│   └── page.tsx          # Main entry page (Home page / Chat UI)
├── components/           # Reusable React components (e.g., Buttons, ChatBubbles, Modals)
├── lib/                  # Utility functions, helpers, and API client integrations
├── public/               # Static assets (images, icons, fonts) - created when needed
├── .gitignore            # Git ignore rules specific to the frontend
├── next.config.ts        # Next.js configuration settings
├── package.json          # Project dependencies and script definitions
├── postcss.config.mjs    # PostCSS config (required for Tailwind)
├── tailwind.config.ts    # Tailwind CSS configuration (theme, colors, etc.)
└── tsconfig.json         # TypeScript configuration
```

## 🚀 Running the Project

To start the development server, run the following commands:

```bash
# Di chuyển vào thư mục frontend
cd frontend

# Cài đặt các package phụ thuộc (nếu chưa cài)
npm install

# Khởi chạy server development
npm run dev
```

The server will be available at `http://localhost:3000`.

## 💡 Best Practices cho Dự án này

1. **Phân chia Components:** Giữ cho các trang trong `app/` thật mỏng (chủ yếu lo việc routing và data fetching). Logic UI chi tiết nên được tách thành các component nhỏ nằm trong thư mục `components/` (ví dụ: `ChatInput.tsx`, `MessageList.tsx`).
2. **Styling:** Ưu tiên sử dụng utility classes của Tailwind CSS trực tiếp vào các thẻ HTML/JSX. Hạn chế viết CSS thuần vào file `globals.css` trừ khi đó là các cài đặt toàn cục (global resets) hoặc biến CSS.
3. **Kết nối API (Backend FastAPI):** Mọi logic gọi API (fetch, axios) kết nối tới backend Python nên được gom vào thư mục `lib/` (ví dụ: `lib/api.ts`) để dễ dàng quản lý, tái sử dụng và thay đổi domain sau này.
4. **TypeScript:** Tận dụng tối đa TypeScript bằng cách định nghĩa các `interface` hoặc `type` cho dữ liệu trả về từ backend để tránh lỗi runtime.
