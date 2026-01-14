import { motion } from 'framer-motion';
import { useState } from 'react';
import { useResponsibilities, useMyResponsibilities, useResponsibilitiesByStatus } from '../../services/responsibilityService';
import type { Responsibility } from '../../types';
import Loading from '../../components/ui/Loading';

const ResponsibilitiesPage = () => {
  const [activeTab, setActiveTab] = useState<'all' | 'my' | 'by-status'>('all');

  const { data: allResponsibilities, isLoading: isLoadingAll, error: errorAll } = useResponsibilities();
  const { data: myResponsibilities, isLoading: isLoadingMy, error: errorMy } = useMyResponsibilities();
  const { data: responsibilitiesByStatus, isLoading: isLoadingByStatus, error: errorByStatus } = useResponsibilitiesByStatus();

  const tabs = [
    { key: 'all' as const, label: 'All Responsibilities', data: allResponsibilities, loading: isLoadingAll, error: errorAll, type: 'list' as const },
    { key: 'my' as const, label: 'My Responsibilities', data: myResponsibilities, loading: isLoadingMy, error: errorMy, type: 'list' as const },
    { key: 'by-status' as const, label: 'By Status', data: responsibilitiesByStatus, loading: isLoadingByStatus, error: errorByStatus, type: 'grouped' as const },
  ];

  const activeTabData = tabs.find(tab => tab.key === activeTab);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800';
      case 'in_progress': return 'bg-blue-100 text-blue-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'on_hold': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return 'bg-red-100 text-red-800';
      case 'high': return 'bg-orange-100 text-orange-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const renderResponsibilities = (responsibilities: Responsibility[] | null) => {
    if (!responsibilities || responsibilities.length === 0) {
      return (
        <div className="text-center py-8">
          <p className="text-gray-500">No responsibilities found.</p>
        </div>
      );
    }

    return (
      <div className="grid gap-4">
        {responsibilities?.map((responsibility) => (
          <motion.div
            key={responsibility.id}
            className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <div className="flex justify-between items-start mb-4">
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{responsibility.title}</h3>
                <p className="text-gray-600 mb-3">{responsibility.description}</p>
                <div className="flex flex-wrap gap-2">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(responsibility.status)}`}>
                    {responsibility.status.replace('_', ' ').toUpperCase()}
                  </span>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(responsibility.priority)}`}>
                    {responsibility.priority.toUpperCase()}
                  </span>
                </div>
              </div>
              <div className="text-right text-sm text-gray-500">
                {responsibility.due_date && (
                  <p>Due: {new Date(responsibility.due_date).toLocaleDateString()}</p>
                )}
                {responsibility.assigned_to_details && (
                  <p>Assigned to: {responsibility.assigned_to_details.first_name} {responsibility.assigned_to_details.last_name}</p>
                )}
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    );
  };

  const renderByStatus = (data: Record<string, Responsibility[]> | null) => {
    if (!data) return null;

    return (
      <div className="space-y-6">
        {Object.entries(data).map(([status, responsibilities]) => (
          <div key={status}>
            <h3 className="text-xl font-semibold text-gray-900 mb-4 capitalize">
              {status.replace('_', ' ')} ({responsibilities.length})
            </h3>
            {renderResponsibilities(responsibilities)}
          </div>
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
        <h1 className="text-3xl font-bold text-gray-900">Responsibilities</h1>
        <p className="text-gray-600 mt-2">Manage and track responsibilities for the farewell event</p>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key as typeof activeTab)}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.key
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Content */}
      <div className="min-h-[400px]">
        {activeTabData?.loading ? (
          <Loading />
        ) : activeTabData?.error ? (
          <div className="text-center py-8">
            <p className="text-red-500">Error loading responsibilities: {activeTabData.error.message}</p>
          </div>
        ) : activeTabData?.type === 'grouped' ? (
          renderByStatus(activeTabData.data as Record<string, Responsibility[]> | null)
        ) : (
          renderResponsibilities(activeTabData?.data as Responsibility[] | null || [])
        )}
      </div>
    </motion.div>
  );
};

export default ResponsibilitiesPage;
