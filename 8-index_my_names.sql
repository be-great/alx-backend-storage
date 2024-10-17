-- optimize simple search
-- index the first letter only of name
CREATE INDEX idx_name_first ON names (name(1));
