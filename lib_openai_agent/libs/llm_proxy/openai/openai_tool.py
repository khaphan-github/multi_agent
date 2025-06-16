# Usage of OpenAI's function calling feature:
'''
  tools = [OpenAITools(
      name="get_list_course_by_topic",
      description="Get Course by topic such as newest course, hottest course, course about office (word, powerppoint, excel,...), contain pricing and free courses.",
      parameters={
          "type": "object",
          "properties": {
              "topic": {
                  "type": "string",
                  "description": "About topic newest course, hottest course, course about office word, powerppoint, excel,..."
              },
              "type": {
                  "type": "string",
                  "description": "Type of course is pricing or free"
              }
          },
          "required": ["topic", "type"]
      },
      instance_function=get_list_course_by_topic  # Ensure this function is defined elsewhere
  )]
'''


class OpenAITools:
    def __init__(self, type: str, enable=True):
        self.type = type
        self.enable = enable  # Ensure enable is properly initialized

    def is_enabled(self):
        """Return the value of the enable property."""
        return self.enable


class OpenAIFunctionCall(OpenAITools):
    def __init__(self, instance_function, name=None, description=None, parameters=None,  enable=True):
        super().__init__(type="function_call", enable=enable)
        if not callable(instance_function):
            raise ValueError(
                "The instance_function must be a callable function.")
        self.name = name
        self.description = description
        self.parameters = parameters
        self.instance_function = instance_function

    def is_enabled(self):
        """Return the value of the enable property."""
        return self.enable


class OpenAIFileSearch(OpenAITools):
    def __init__(self, enable=True):
        super().__init__(type="file_search", enable=enable)


class OpenAICodeInterpreter(OpenAITools):
    def __init__(self, enable=True):
        super().__init__(type="code_interpreter", enable=enable)
