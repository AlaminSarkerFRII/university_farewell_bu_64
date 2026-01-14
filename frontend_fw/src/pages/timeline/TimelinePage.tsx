import { motion } from 'framer-motion';
import { useState } from 'react';
import { useTimelines, useTimelineEvents } from '../../services/timelineService';
import type { TimelineEvent } from '../../types';
import Loading from '../../components/ui/Loading';
import { Calendar, Clock, MapPin } from 'lucide-react';

const TimelinePage = () => {
  const [selectedTimelineId, setSelectedTimelineId] = useState<number | null>(null);

  const { data: timelines, isLoading: isLoadingTimelines, error: errorTimelines } = useTimelines();
  const { data: selectedTimelineEvents, isLoading: isLoadingEvents, error: errorEvents } = useTimelineEvents(selectedTimelineId || 0);

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'pre_event': return 'bg-blue-100 text-blue-800';
      case 'main_event': return 'bg-purple-100 text-purple-800';
      case 'post_event': return 'bg-green-100 text-green-800';
      case 'other': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const renderTimelinesList = () => {
    if (isLoadingTimelines) return <Loading />;
    if (errorTimelines) return <div className="text-red-500">Error loading timelines: {errorTimelines.message}</div>;
    if (!timelines || timelines.length === 0) return <div className="text-gray-500">No timelines found.</div>;

    return (
      <div className="grid gap-4">
        {timelines.map((timeline) => (
          <motion.div
            key={timeline.id}
            className={`bg-white rounded-lg shadow p-6 cursor-pointer hover:shadow-md transition-shadow ${
              selectedTimelineId === timeline.id ? 'ring-2 ring-blue-500' : ''
            }`}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            onClick={() => setSelectedTimelineId(selectedTimelineId === timeline.id ? null : timeline.id)}
          >
            <div className="flex justify-between items-start mb-4">
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{timeline.title}</h3>
                <p className="text-gray-600 mb-3">{timeline.description}</p>
                <div className="flex flex-wrap gap-2">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getCategoryColor(timeline.category)}`}>
                    {timeline.category.replace('_', ' ').toUpperCase()}
                  </span>
                  {timeline.is_featured && (
                    <span className="px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                      FEATURED
                    </span>
                  )}
                  {timeline.is_published ? (
                    <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      PUBLISHED
                    </span>
                  ) : (
                    <span className="px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                      DRAFT
                    </span>
                  )}
                </div>
              </div>
              <div className="text-right text-sm text-gray-500">
                <p>Start: {new Date(timeline.start_date).toLocaleDateString()}</p>
                {timeline.end_date && <p>End: {new Date(timeline.end_date).toLocaleDateString()}</p>}
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    );
  };

  const renderTimelineEvents = (events: TimelineEvent[] | undefined) => {
    if (!events || events.length === 0) {
      return (
        <div className="text-center py-8">
          <p className="text-gray-500">No events found for this timeline.</p>
        </div>
      );
    }

    return (
      <div className="space-y-4">
        {events
          .sort((a, b) => new Date(a.event_date).getTime() - new Date(b.event_date).getTime())
          .map((event) => (
            <motion.div
              key={event.id}
              className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="flex items-start space-x-4">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                    <Calendar className="w-6 h-6 text-blue-600" />
                  </div>
                </div>
                <div className="flex-1">
                  <h4 className="text-lg font-semibold text-gray-900 mb-2">{event.title}</h4>
                  <p className="text-gray-600 mb-3">{event.description}</p>
                  <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500">
                    <div className="flex items-center">
                      <Clock className="w-4 h-4 mr-1" />
                      {new Date(event.event_date).toLocaleDateString()} at {new Date(event.event_date).toLocaleTimeString()}
                    </div>
                    {event.location && (
                      <div className="flex items-center">
                        <MapPin className="w-4 h-4 mr-1" />
                        {event.location}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
      </div>
    );
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
    >
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Timeline</h1>
        <p className="text-gray-600 mt-2">Manage event timelines and schedules</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Timelines List */}
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Timelines</h2>
          <div className="min-h-[400px]">
            {renderTimelinesList()}
          </div>
        </div>

        {/* Selected Timeline Events */}
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            {selectedTimelineId ? 'Timeline Events' : 'Select a timeline to view events'}
          </h2>
          <div className="min-h-[400px]">
            {selectedTimelineId ? (
              isLoadingEvents ? (
                <Loading />
              ) : errorEvents ? (
                <div className="text-red-500">Error loading events: {errorEvents.message}</div>
              ) : (
                renderTimelineEvents(selectedTimelineEvents)
              )
            ) : (
              <div className="flex items-center justify-center h-full text-gray-500">
                <div className="text-center">
                  <Calendar className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                  <p>Select a timeline to view its events</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default TimelinePage;
