import { motion } from 'framer-motion';

const ResponsibilitiesPage = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <h1 className="text-3xl font-bold text-gray-900">Responsibilities</h1>
      <p className="text-gray-600 mt-2">Responsibilities management functionality coming soon</p>
    </motion.div>
  );
};

export default ResponsibilitiesPage;
