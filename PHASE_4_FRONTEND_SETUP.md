# Phase 4 - Frontend Development with React + Vite

## 🚀 Phase 4 Overview

**Objective**: Build a modern React frontend using Vite with TypeScript integration.

**Tech Stack**:
- React 18
- TypeScript
- Vite (build tool)
- React Router (navigation)
- React Query / TanStack Query (state management)
- Axios (HTTP client)
- Ant Design / TailwindCSS (styling)
- ESLint + Prettier (code quality)

**Timeline**: 4-6 weeks

---

## 📋 Phase 4 Deliverables

### Core Features
- ✅ Authentication system (register, login, logout)
- ✅ Dashboard with timeline view
- ✅ User profile management
- ✅ Timeline management (create, edit, publish)
- ✅ Responsibilities management with drag-and-drop
- ✅ Real-time updates with WebSockets (future)
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Admin panel

### Technical Requirements
- ✅ TypeScript for type safety
- ✅ Component composition architecture
- ✅ Custom hooks for reusability
- ✅ API client with interceptors
- ✅ Error handling & validation
- ✅ Testing (Jest + React Testing Library)
- ✅ Performance optimization
- ✅ Accessibility (WCAG 2.1)

---

## 🏗️ Project Structure

```
frontend/
├── public/
│   ├── favicon.ico
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Auth/
│   │   │   ├── LoginForm.tsx
│   │   │   ├── RegisterForm.tsx
│   │   │   └── ProtectedRoute.tsx
│   │   ├── Timeline/
│   │   │   ├── TimelineList.tsx
│   │   │   ├── TimelineForm.tsx
│   │   │   ├── TimelineCard.tsx
│   │   │   └── TimelineDetail.tsx
│   │   ├── Responsibility/
│   │   │   ├── ResponsibilityBoard.tsx
│   │   │   ├── ResponsibilityCard.tsx
│   │   │   └── ResponsibilityForm.tsx
│   │   ├── User/
│   │   │   ├── ProfileCard.tsx
│   │   │   ├── UserForm.tsx
│   │   │   └── UserList.tsx
│   │   ├── Layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Footer.tsx
│   │   └── Common/
│   │       ├── Button.tsx
│   │       ├── Modal.tsx
│   │       └── Toast.tsx
│   ├── pages/
│   │   ├── Login.tsx
│   │   ├── Register.tsx
│   │   ├── Dashboard.tsx
│   │   ├── Timelines.tsx
│   │   ├── Responsibilities.tsx
│   │   ├── Profile.tsx
│   │   ├── Admin.tsx
│   │   └── NotFound.tsx
│   ├── services/
│   │   ├── api.ts (Axios client)
│   │   ├── auth.ts (Auth API calls)
│   │   ├── timelines.ts (Timeline API calls)
│   │   ├── responsibilities.ts (Responsibility API calls)
│   │   └── users.ts (User API calls)
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useTimelines.ts
│   │   ├── useResponsibilities.ts
│   │   ├── useFetch.ts
│   │   └── useLocalStorage.ts
│   ├── context/
│   │   ├── AuthContext.tsx
│   │   └── AppContext.tsx
│   ├── types/
│   │   ├── index.ts (TypeScript types)
│   │   ├── models.ts
│   │   └── api.ts
│   ├── utils/
│   │   ├── constants.ts
│   │   ├── helpers.ts
│   │   ├── formatters.ts
│   │   └── validators.ts
│   ├── styles/
│   │   ├── globals.css
│   │   ├── App.css
│   │   └── themes.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── vite-env.d.ts
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── .env.example
├── .eslintrc.cjs
├── .prettierrc
├── tsconfig.json
├── vite.config.ts
├── package.json
└── README.md
```

---

## 🛠️ Setup Instructions

### 1. Create Vite React Project
```bash
# Create new Vite project with React + TypeScript
npm create vite@latest frontend -- --template react-ts

cd frontend

# Install dependencies
npm install
```

### 2. Install Required Packages
```bash
# Core dependencies
npm install react-router-dom@6.20.0
npm install @tanstack/react-query@5.25.0
npm install axios@1.6.2
npm install zustand@4.4.0  # or Redux Toolkit

# UI Framework
npm install antd@5.11.0
npm install @ant-design/icons@5.2.6

# CSS Utilities
npm install tailwindcss@3.3.6
npm install postcss@8.4.32
npm install autoprefixer@10.4.16

# Development dependencies
npm install -D typescript@5.3.3
npm install -D eslint@8.55.0
npm install -D eslint-config-react-app
npm install -D prettier@3.1.1
npm install -D @types/react@18.2.37
npm install -D @types/react-dom@18.2.15

# Testing
npm install -D vitest@0.34.6
npm install -D @testing-library/react@14.1.2
npm install -D @testing-library/jest-dom@6.1.5
npm install -D @testing-library/user-event@14.5.1

# Environment management
npm install dotenv@16.3.1
```

### 3. Configure Tailwind CSS
```bash
# Generate Tailwind config
npx tailwindcss init -p
```

**tailwind.config.js**:
```javascript
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

**src/styles/globals.css**:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### 4. Setup Environment Variables
Create `.env.local`:
```env
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=Versity Farewell
VITE_APP_VERSION=1.0.0
```

Create `.env.example`:
```env
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=Versity Farewell
VITE_APP_VERSION=1.0.0
```

### 5. Create API Client Service

**src/services/api.ts**:
```typescript
import axios, { AxiosInstance, AxiosError } from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

class ApiClient {
  private client: AxiosInstance;
  private refreshPromise: Promise<string> | null = null;

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as any;

        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          if (!this.refreshPromise) {
            this.refreshPromise = this.refreshAccessToken();
          }

          try {
            const newToken = await this.refreshPromise;
            originalRequest.headers.Authorization = `Bearer ${newToken}`;
            return this.client(originalRequest);
          } catch (refreshError) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.href = '/login';
            return Promise.reject(refreshError);
          } finally {
            this.refreshPromise = null;
          }
        }

        return Promise.reject(error);
      }
    );
  }

  private async refreshAccessToken(): Promise<string> {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    try {
      const response = await axios.post(`${API_URL}/token/refresh/`, {
        refresh: refreshToken,
      });
      const { access } = response.data;
      localStorage.setItem('access_token', access);
      return access;
    } catch (error) {
      throw new Error('Token refresh failed');
    }
  }

  get<T>(url: string, config?: any) {
    return this.client.get<T>(url, config);
  }

  post<T>(url: string, data?: any, config?: any) {
    return this.client.post<T>(url, data, config);
  }

  put<T>(url: string, data?: any, config?: any) {
    return this.client.put<T>(url, data, config);
  }

  patch<T>(url: string, data?: any, config?: any) {
    return this.client.patch<T>(url, data, config);
  }

  delete<T>(url: string, config?: any) {
    return this.client.delete<T>(url, config);
  }
}

export default new ApiClient();
```

### 6. Create TypeScript Types

**src/types/index.ts**:
```typescript
export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: 'student' | 'organizer' | 'treasurer' | 'admin';
  is_active: boolean;
  created_at: string;
}

export interface Timeline {
  id: string;
  title: string;
  description: string;
  category: string;
  start_date: string;
  end_date: string;
  is_published: boolean;
  is_featured: boolean;
  created_by: User;
  created_at: string;
  updated_at: string;
}

export interface Responsibility {
  id: string;
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  status: 'pending' | 'in_progress' | 'completed' | 'on_hold';
  assigned_to: User | null;
  category: string;
  due_date: string;
  created_at: string;
  updated_at: string;
}

export interface AuthResponse {
  message: string;
  user: User;
  access: string;
  refresh: string;
}
```

### 7. Create Custom Hooks

**src/hooks/useAuth.ts**:
```typescript
import { useState, useCallback, useEffect } from 'react';
import { User, AuthResponse } from '../types';
import api from '../services/api';

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      fetchProfile();
    }
  }, []);

  const fetchProfile = async () => {
    try {
      setLoading(true);
      const response = await api.get('/users/profile/');
      setUser(response.data);
    } catch (err) {
      setError('Failed to fetch profile');
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = useCallback(async (email: string, password: string) => {
    try {
      setLoading(true);
      const response = await api.post<AuthResponse>('/auth/login/', {
        email,
        password,
      });
      const { user, access, refresh } = response.data;
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      setUser(user);
      return user;
    } catch (err) {
      setError('Login failed');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
  }, []);

  return {
    user,
    loading,
    error,
    login,
    logout,
    isAuthenticated: !!user,
  };
}
```

---

## 🎨 Component Templates

### Login Component
**src/components/Auth/LoginForm.tsx**:
```typescript
import { useState } from 'react';
import { Form, Input, Button, Card, message } from 'antd';
import { useAuth } from '../../hooks/useAuth';
import { useNavigate } from 'react-router-dom';

export default function LoginForm() {
  const { login, loading } = useAuth();
  const navigate = useNavigate();
  const [form] = Form.useForm();

  const handleSubmit = async (values: any) => {
    try {
      await login(values.email, values.password);
      message.success('Login successful!');
      navigate('/dashboard');
    } catch (error) {
      message.error('Login failed. Please try again.');
    }
  };

  return (
    <Card title="Login" style={{ maxWidth: 400 }} className="mx-auto mt-16">
      <Form form={form} onFinish={handleSubmit} layout="vertical">
        <Form.Item
          name="email"
          label="Email"
          rules={[
            { required: true, message: 'Please enter your email' },
            { type: 'email', message: 'Invalid email format' },
          ]}
        >
          <Input type="email" placeholder="you@example.com" />
        </Form.Item>
        <Form.Item
          name="password"
          label="Password"
          rules={[{ required: true, message: 'Please enter your password' }]}
        >
          <Input.Password placeholder="••••••••" />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit" block loading={loading}>
            Login
          </Button>
        </Form.Item>
      </Form>
    </Card>
  );
}
```

### Protected Route Component
**src/components/Auth/ProtectedRoute.tsx**:
```typescript
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

interface Props {
  children: React.ReactNode;
  requiredRole?: string;
}

export default function ProtectedRoute({ children, requiredRole }: Props) {
  const { user, loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (requiredRole && user.role !== requiredRole) {
    return <Navigate to="/" replace />;
  }

  return <>{children}</>;
}
```

---

## 📦 Build & Deploy

### Development
```bash
npm run dev
# Server runs at http://localhost:5173
```

### Production Build
```bash
npm run build
npm run preview
```

### Docker Setup (Future)
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## 🚀 Implementation Roadmap

### Week 1: Setup & Auth
- [x] Create Vite project
- [ ] Configure TypeScript
- [ ] Setup API client
- [ ] Implement Auth pages
- [ ] Create custom hooks

### Week 2: Core Features
- [ ] Dashboard page
- [ ] Timeline list & detail
- [ ] Timeline CRUD operations
- [ ] Responsibility board
- [ ] User profile

### Week 3: Advanced Features
- [ ] Drag-and-drop for responsibilities
- [ ] Search & filtering
- [ ] Real-time notifications
- [ ] File uploads

### Week 4: Polish & Testing
- [ ] Unit tests
- [ ] Integration tests
- [ ] Performance optimization
- [ ] Accessibility audit
- [ ] Documentation

### Week 5-6: Deployment
- [ ] Docker setup
- [ ] CI/CD pipeline
- [ ] Production deployment
- [ ] Monitoring setup

---

## ✅ Checklist

- [ ] Vite project created
- [ ] Dependencies installed
- [ ] Environment configured
- [ ] API client setup
- [ ] TypeScript types defined
- [ ] Custom hooks created
- [ ] Auth pages implemented
- [ ] Protected routes working
- [ ] API integration tested
- [ ] Components documented
- [ ] Build process verified
- [ ] Ready for deployment

---

**Next Step**: Execute setup instructions and confirm frontend environment is ready.

