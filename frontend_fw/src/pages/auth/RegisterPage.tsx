import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

const RegisterPage = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <h1 className="text-3xl font-bold text-gray-900">Register</h1>
      <p className="text-gray-600 mt-2">
        Registration functionality coming soon. <Link to="/login">Go back to login</Link>
      </p>
    </motion.div>
  );
};

export default RegisterPage;
