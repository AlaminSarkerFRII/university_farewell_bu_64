import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import axiosInstance from '../lib/axios';
import type { Timeline, TimelineEvent } from '../types';

// Timeline API calls
export const timelineApi = {
  getTimelines: async (filters?: Record<string, string>): Promise<Timeline[]> => {
    const params = new URLSearchParams(filters);
    const { data } = await axiosInstance.get(`/timelines/?${params}`);
    return data.results || [];
  },

  getTimeline: async (id: number): Promise<Timeline> => {
    const { data } = await axiosInstance.get(`/timelines/${id}/`);
    return data;
  },

  createTimeline: async (timeline: Partial<Timeline>): Promise<Timeline> => {
    const { data } = await axiosInstance.post('/timelines/', timeline);
    return data;
  },

  updateTimeline: async ({ id, ...timeline }: Partial<Timeline> & { id: number }): Promise<Timeline> => {
    const { data } = await axiosInstance.put(`/timelines/${id}/`, timeline);
    return data;
  },

  deleteTimeline: async (id: number): Promise<void> => {
    await axiosInstance.delete(`/timelines/${id}/`);
  },

  publishTimeline: async (id: number): Promise<void> => {
    await axiosInstance.post(`/timelines/${id}/publish/`);
  },

  getTimelineEvents: async (timelineId: number): Promise<TimelineEvent[]> => {
    const { data } = await axiosInstance.get(`/timelines/${timelineId}/events/`);
    return data;
  },

  createTimelineEvent: async (event: Partial<TimelineEvent>): Promise<TimelineEvent> => {
    const { data } = await axiosInstance.post('/timeline-events/', event);
    return data;
  },

  updateTimelineEvent: async ({ id, ...event }: Partial<TimelineEvent> & { id: number }): Promise<TimelineEvent> => {
    const { data } = await axiosInstance.put(`/timeline-events/${id}/`, event);
    return data;
  },

  deleteTimelineEvent: async (id: number): Promise<void> => {
    await axiosInstance.delete(`/timeline-events/${id}/`);
  },
};

// React Query Hooks
export const useTimelines = (filters?: Record<string, string>) => {
  return useQuery({
    queryKey: ['timelines', filters],
    queryFn: () => timelineApi.getTimelines(filters),
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
};

export const useTimeline = (id: number) => {
  return useQuery({
    queryKey: ['timeline', id],
    queryFn: () => timelineApi.getTimeline(id),
    enabled: !!id,
    staleTime: 2 * 60 * 1000,
  });
};

export const useCreateTimeline = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: timelineApi.createTimeline,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['timelines'] });
    },
  });
};

export const useUpdateTimeline = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: timelineApi.updateTimeline,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['timelines'] });
      queryClient.invalidateQueries({ queryKey: ['timeline', data.id] });
    },
  });
};

export const useDeleteTimeline = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: timelineApi.deleteTimeline,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['timelines'] });
    },
  });
};

export const usePublishTimeline = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: timelineApi.publishTimeline,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['timelines'] });
    },
  });
};

export const useTimelineEvents = (timelineId: number) => {
  return useQuery({
    queryKey: ['timelineEvents', timelineId],
    queryFn: () => timelineApi.getTimelineEvents(timelineId),
    enabled: !!timelineId,
    staleTime: 2 * 60 * 1000,
  });
};

export const useCreateTimelineEvent = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: timelineApi.createTimelineEvent,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['timelineEvents', data.timeline] });
      queryClient.invalidateQueries({ queryKey: ['timelines'] });
    },
  });
};

export const useUpdateTimelineEvent = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: timelineApi.updateTimelineEvent,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['timelineEvents', data.timeline] });
    },
  });
};

export const useDeleteTimelineEvent = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: timelineApi.deleteTimelineEvent,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['timelineEvents'] });
      queryClient.invalidateQueries({ queryKey: ['timelines'] });
    },
  });
};
