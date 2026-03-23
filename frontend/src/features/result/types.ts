export type Result = {
  id: string;
  year: number;
  exam_type: string;
  pass_rate: number;
};

export type ResultCreatePayload = {
  school_id?: string;
  year: number;
  exam_type: string;
  pass_rate: number;
};

export type ResultUpdatePayload = Partial<ResultCreatePayload>;
