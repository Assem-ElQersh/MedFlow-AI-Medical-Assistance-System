import { z } from 'zod';

// Common validation schemas
export const emailSchema = z.string().email('Invalid email address');

export const passwordSchema = z
  .string()
  .min(8, 'Password must be at least 8 characters')
  .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
  .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
  .regex(/[0-9]/, 'Password must contain at least one number')
  .regex(/[^A-Za-z0-9]/, 'Password must contain at least one special character');

export const phoneSchema = z
  .string()
  .regex(/^\+?[1-9]\d{1,14}$/, 'Invalid phone number format');

export const dateSchema = z.string().refine((date) => {
  const parsedDate = new Date(date);
  return !isNaN(parsedDate.getTime());
}, 'Invalid date format');

// Patient validation schemas
export const patientSchema = z.object({
  fullName: z.string().min(2, 'Name must be at least 2 characters'),
  email: emailSchema,
  dateOfBirth: dateSchema,
  gender: z.enum(['male', 'female', 'other']),
  phone: phoneSchema,
  address: z.string().min(5, 'Address must be at least 5 characters'),
});

// Emergency contact validation schema
export const emergencyContactSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  relationship: z.string().min(2, 'Relationship must be at least 2 characters'),
  phone: phoneSchema,
});

// Diagnosis validation schema
export const diagnosisSchema = z.object({
  patientId: z.string().uuid('Invalid patient ID'),
  symptoms: z.array(
    z.object({
      name: z.string().min(2, 'Symptom name must be at least 2 characters'),
      severity: z.enum(['mild', 'moderate', 'severe']),
    })
  ).min(1, 'At least one symptom is required'),
});

// Appointment validation schema
export const appointmentSchema = z.object({
  specialistId: z.string().uuid('Invalid specialist ID'),
  patientId: z.string().uuid('Invalid patient ID'),
  date: dateSchema,
  time: z.string().regex(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/, 'Invalid time format'),
  reason: z.string().min(10, 'Reason must be at least 10 characters'),
  urgency: z.enum(['routine', 'urgent', 'emergency']),
});

// Validation utility functions
export const validateField = <T>(
  schema: z.ZodType<T>,
  value: unknown
): { isValid: boolean; error?: string } => {
  try {
    schema.parse(value);
    return { isValid: true };
  } catch (error) {
    if (error instanceof z.ZodError) {
      return {
        isValid: false,
        error: error.errors[0].message,
      };
    }
    return {
      isValid: false,
      error: 'Validation failed',
    };
  }
};

export const validateForm = <T>(
  schema: z.ZodType<T>,
  data: unknown
): { isValid: boolean; errors?: Record<string, string> } => {
  try {
    schema.parse(data);
    return { isValid: true };
  } catch (error) {
    if (error instanceof z.ZodError) {
      const errors: Record<string, string> = {};
      error.errors.forEach((err) => {
        const path = err.path.join('.');
        errors[path] = err.message;
      });
      return {
        isValid: false,
        errors,
      };
    }
    return {
      isValid: false,
      errors: {
        _form: 'Validation failed',
      },
    };
  }
};

// Custom validation rules
export const customRules = {
  isFutureDate: (date: string) => {
    const parsedDate = new Date(date);
    return parsedDate > new Date();
  },
  isWithinRange: (value: number, min: number, max: number) => {
    return value >= min && value <= max;
  },
  isStrongPassword: (password: string) => {
    return passwordSchema.safeParse(password).success;
  },
  isValidPhoneNumber: (phone: string) => {
    return phoneSchema.safeParse(phone).success;
  },
  isAdult: (dateOfBirth: string) => {
    const birthDate = new Date(dateOfBirth);
    const today = new Date();
    const age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
      return age - 1 >= 18;
    }
    return age >= 18;
  },
};

// Error message formatter
export const formatErrorMessage = (field: string, error: string): string => {
  return `${field.charAt(0).toUpperCase() + field.slice(1)}: ${error}`;
};

// Validation hooks
export const useValidation = <T>(schema: z.ZodType<T>) => {
  const validate = (data: unknown) => validateForm(schema, data);
  const validateField = (field: string, value: unknown) => {
    const fieldSchema = schema.shape?.[field];
    if (fieldSchema) {
      return validateField(fieldSchema, value);
    }
    return { isValid: true };
  };

  return {
    validate,
    validateField,
  };
}; 