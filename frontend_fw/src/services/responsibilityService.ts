import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import axiosInstance from '../lib/axios';
import type { Responsibility, ResponsibilityCategory } from '../types';

// Responsibility API calls
export const responsibilityApi = {
  getResponsibilities: async (filters?: Record<string, string>): Promise<Responsibility[]> => {
    const params = new URLSearchParams(filters);
    const { data } = await axiosInstance.get(`/responsibilities/?${params}`);
    // Handle paginated response
    return data.results || data;
  },

  getResponsibility: async (id: number): Promise<Responsibility> => {
    const { data } = await axiosInstance.get(`/responsibilities/${id}/`);
    return data;
  },

  createResponsibility: async (responsibility: Partial<Responsibility>): Promise<Responsibility> => {
    const { data } = await axiosInstance.post('/responsibilities/', responsibility);
    return data;
  },

  updateResponsibility: async ({ id, ...responsibility }: Partial<Responsibility> & { id: number }): Promise<Responsibility> => {
    const { data } = await axiosInstance.patch(`/responsibilities/${id}/`, responsibility);
    return data;
  },

  deleteResponsibility: async (id: number): Promise<void> => {
    await axiosInstance.delete(`/responsibilities/${id}/`);
  },

  updateStatus: async ({ id, status }: { id: number; status: string }): Promise<Responsibility> => {
    const { data } = await axiosInstance.patch(`/responsibilities/${id}/update_status/`, { status });
    return data;
  },

  assignTo: async ({ id, user_id }: { id: number; user_id: number }): Promise<Responsibility> => {
    const { data } = await axiosInstance.post(`/responsibilities/${id}/assign_to/`, { user_id });
    return data;
  },

  getMyResponsibilities: async (): Promise<Responsibility[]> => {
    const { data } = await axiosInstance.get('/responsibilities/my_responsibilities/');
    return data;
  },

  getByStatus: async (): Promise<Record<string, Responsibility[]>> => {
    const { data } = await axiosInstance.get('/responsibilities/by_status/');
    return data;
  },

  getByPriority: async (): Promise<Record<string, Responsibility[]>> => {
    const { data } = await axiosInstance.get('/responsibilities/by_priority/');
    return data;
  },

  // Categories
  getCategories: async (): Promise<ResponsibilityCategory[]> => {
    const { data } = await axiosInstance.get('/responsibility-categories/');
    // Handle paginated response
    return data.results || data;
  },

  createCategory: async (category: Partial<ResponsibilityCategory>): Promise<ResponsibilityCategory> => {
    const { data } = await axiosInstance.post('/responsibility-categories/', category);
    return data;
  },
};

// React Query Hooks
export const useResponsibilities = (filters?: Record<string, string>) => {
  return useQuery({
    queryKey: ['responsibilities', filters],
    queryFn: () => responsibilityApi.getResponsibilities(filters),
    staleTime: 1 * 60 * 1000, // 1 minute
  });
};

export const useResponsibility = (id: number) => {
  return useQuery({
    queryKey: ['responsibility', id],
    queryFn: () => responsibilityApi.getResponsibility(id),
    enabled: !!id,
    staleTime: 1 * 60 * 1000,
  });
};

export const useCreateResponsibility = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: responsibilityApi.createResponsibility,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['responsibilities'] });
    },
  });
};

export const useUpdateResponsibility = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: responsibilityApi.updateResponsibility,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['responsibilities'] });
      queryClient.invalidateQueries({ queryKey: ['responsibility', data.id] });
    },
  });
};

export const useDeleteResponsibility = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: responsibilityApi.deleteResponsibility,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['responsibilities'] });
    },
  });
};

export const useUpdateResponsibilityStatus = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: responsibilityApi.updateStatus,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['responsibilities'] });
      queryClient.invalidateQueries({ queryKey: ['responsibility', data.id] });
      queryClient.invalidateQueries({ queryKey: ['myResponsibilities'] });
    },
  });
};

export const useAssignResponsibility = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: responsibilityApi.assignTo,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['responsibilities'] });
      queryClient.invalidateQueries({ queryKey: ['responsibility', data.id] });
    },
  });
};

export const useMyResponsibilities = () => {
  return useQuery({
    queryKey: ['myResponsibilities'],
    queryFn: responsibilityApi.getMyResponsibilities,
    staleTime: 1 * 60 * 1000,
  });
};

export const useResponsibilitiesByStatus = () => {
  return useQuery({
    queryKey: ['responsibilitiesByStatus'],
    queryFn: responsibilityApi.getByStatus,
    staleTime: 1 * 60 * 1000,
  });
};

export const useResponsibilitiesByPriority = () => {
  return useQuery({
    queryKey: ['responsibilitiesByPriority'],
    queryFn: responsibilityApi.getByPriority,
    staleTime: 1 * 60 * 1000,
  });
};

export const useResponsibilityCategories = () => {
  return useQuery({
    queryKey: ['responsibilityCategories'],
    queryFn: responsibilityApi.getCategories,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useCreateCategory = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: responsibilityApi.createCategory,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['responsibilityCategories'] });
    },
  });
};
